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
    problem_count = None
    
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
    
        # Check if this user has already got a passing state for this problem
        if not cache.get(f'workshop_{self.workshop_id}_problem_{self.problem.id}_session_{self.session_id}_passed', default=False):
            with await sync_to_async(open)(self.submission.code.path, 'rb') as f:
                source_code = await sync_to_async(f.read)()
    
            loop = asyncio.get_event_loop()
            problemtestset = await database_sync_to_async(self.problem.problemtest_set.all)()
            self.problem_count = await database_sync_to_async(problemtestset.count)()
            for test in problemtestset:
                loop.create_task(self.test_submit(source_code, test))
        else:
            # TODO: Give the user a message saying they have already submitted the problem
            pass

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

        await self.requeue_waiting(test_result)

    async def requeue_waiting(self, test_result):
        # If we don't have an actual result yet, then
        if test_result.result_data["status"]["id"] in [1, 2]:
            await self.test_schedule(test_result)
        else:
            # We are on a final state, so we can inform whatever
            await sync_to_async(self.on_test_final)(test_result)

    async def test_reload(self, test_result):
        data = await sync_to_async(api.submission.get)(client, test_result.result_data["token"])
        if data.status["id"] != test_result.result_data["status"]["id"]:
            test_result.result_data.update(**dict(data))
            await database_sync_to_async(test_result.save)()
            await sync_to_async(test_result.send_user_status)(self.channel_name)
            await self.requeue_waiting(test_result)

        else:
            await self.test_schedule(test_result)

    async def test_schedule(self, test_result):
        await asyncio.sleep(0.5)
        await self.test_reload(test_result)

    def on_test_final(self, test_result):
        """
        Called when the test reaches a final state (aka not queued or running)
        :param test_result:
        :return:
        """
        
        session_id = test_result.submission.options["session_id"]
        workshop_id = test_result.submission.workshop_id
        problem_id = test_result.test.problem_id
        submission_id = test_result.submission_id
        
        # Has many tests has this user passed for this problem
        previous_attempt = cache.get(f"workshop_{workshop_id}_problem_{problem_id}_session_{session_id}_attempted", default=False)
        
        if not previous_attempt:
            # This is the first test that has hit the final state for this user and problem
            cache.set (f"workshop_{workshop_id}_problem_{problem_id}_session_{session_id}_attempted", True)
            cache.incr(f'workshop_{workshop_id}_problem_{problem_id}_users_attempted')
        else:
            # The user has submitted the problem again, or another test has finished
            pass
        
        # How many tests for this submission have passed?
        cache.get_or_set(f"workshop_{workshop_id}_submission_{submission_id}_passes", 0)
        if test_result.result_data["status"]["id"] == 3:  # 3 means accepted
            submission_passes = cache.incr(f"workshop_{workshop_id}_submission_{submission_id}_passes")
            
            if submission_passes == self.problem_count:
                # The user has solved the problem
                cache.incr(f'workshop_{workshop_id}_problem_{problem_id}_users_attempted')
                cache.set(f'workshop_{workshop_id}_problem_{problem_id}_session_{session_id}_passed', True)
                # TODO: Send a success message
        
        
            
        


