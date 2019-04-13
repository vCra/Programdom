import asyncio
import logging

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache

from channels.layers import get_channel_layer
import judge0api as api
from programdom.bridge.client import client
from programdom.models import SubmissionTestResult, Submission

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


class ProgramdomBridgeConsumer(AsyncConsumer):
    submission = None
    problem = None
    workshop_id = None
    session_id = None
    channel_name = None

    async def evaluate(self, message):
        """
        Sends a message to judge0api, and then processes the result
        :param message: a dict containing the following:
            message = {
                "type": "solution.evaluate", # To match to this method
                "submission_id": the PK of the submission object
                "session_id": The clients session_id - used to send messages back to the user
                "workshop_id": the PK of the workshop associated with this submission - used for stats tracking
            }
        """
        self.submission = await database_sync_to_async(Submission.objects.get)(pk=message["submission_id"])
        self.problem = self.submission.problem
        self.workshop_id = self.submission.workshop.id
        self.session_id = message["session_id"]
        self.channel_name = await sync_to_async(cache.get)(f"session_{self.session_id}_channel-name")

        logger.debug(f"Evaluating {self.submission}")

        with await sync_to_async(open)(self.submission.code.path, 'rb') as f:
            source_code = await sync_to_async(f.read)()

        loop = asyncio.get_event_loop()
        for test in await database_sync_to_async(self.problem.problemtest_set.all)():
            loop.create_task(self.test_submit(source_code, test))

    async def test_submit(self, source_code, test):
        submission = await sync_to_async(api.submission.submit)(
            client,
            source_code,
            self.problem.language.judge_zero_id,
            stdin=test.std_in.encode(),
            expected_output=test.std_out.encode()
        )
        await sync_to_async(submission.load)(client)
        logger.debug(f"Running test {test} for {self.submission}")

        # TODO: Cleanup
        test_result = await database_sync_to_async(SubmissionTestResult)(submission=self.submission, test=test, result_data=dict(submission))
        await database_sync_to_async(test_result.save)()
        await sync_to_async(test_result.send_user_status)(self.channel_name)

        # If we don't have an actual result yet, then
        if test_result.result_data["status"]["id"] in [1, 2]:
            await self.test_schedule(test_result)

    async def test_reload(self, test):
        data = await sync_to_async(api.submission.get)(client, test.result_data["token"])
        if data.status["id"] != test.result_data["status"]["id"]:
            test.result_data.update(**dict(data))
            await database_sync_to_async(test.save)()
            await sync_to_async(test.send_user_status)(self.channel_name)
            if data.status["id"] in [2]:
                await self.test_schedule(test)
        else:
            await self.test_schedule(test)

    async def test_schedule(self, test):
        await asyncio.sleep(0.5)
        await self.test_reload(test)
