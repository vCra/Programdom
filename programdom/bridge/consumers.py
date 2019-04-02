import asyncio
import os
from pprint import pprint

import aiofiles as aiofiles
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from django.core.cache import cache

from channels.layers import get_channel_layer
from django.conf import settings
import judge0api as api
from programdom.bridge.client import client
from programdom.models import Problem, SubmissionTestResult

channel_layer = get_channel_layer()

class ProgramdomBridgeConsumer(AsyncConsumer):

    problem = None
    workshop_id = None
    session_id = None
    channel_name = None
    file = None

    async def evaluate(self, message):
        """
        Sends a message to judge0api, and then processes the result
        :param message: a dict containing the following:
            message = {
                "type": "solution.evaluate", # To match to this method
                "problem_id": The Mooshak ID of the problem this solution is for
                "code_url": The URL of the code for this submission
                "session_id": The clients session_id - used to send messages back to the user
                "workshop_id": the PK of the workshop associated with this submission - used for stats tracking
            }
        """

        self.problem = Problem.objects.get(id=message["problem_id"])
        self.workshop_id = message["workshop_id"]
        self.session_id = message["session_id"]
        self.channel_name = cache.get(f"session_{self.session_id}_channel-name")

        url = message["code_url"]


        # Our old system downloaded files and then sent them off. We will probably go back to this once in prod and have
        # an actual object storage system working. However, ATM we can just use the local files.

        # async with aiohttp.ClientSession() as session:
        #     # TODO: Check file is accessable (aka http 200)
        #     async with session.get(f"{url}") as response:
        #         data = await response.read()

        # TODO: This is horrible, and should be changed
        async with aiofiles.open(str(settings.APPS_DIR(url[1:])), mode='rb') as f:
            self.file = await f.read()

        for test in self.problem.problemtest_set.all():
            submission = sync_to_async(api.submission.submit)(client, self.file, self.problem.language.judge_zero_id, stdin=test.std_in, expected_output=test.std_out)

            client_result = dict(vars(submission))

            await self.handle_state(client_result)

            test_result = SubmissionTestResult()

            client_result.update({"type": "submission.status"})
            client_result.update({"test": test})


    async def handle_state(self, message):
        # Sends a message to the end user saying what is happening
        await channel_layer.send(self.channel_name, message)
        # Update the lecturers graph
        await channel_layer.group_send(f"workshop_{self.workshop_id}_control", {"type": "graph.update"})

    def submit_allowed(self):
        """
        Checks if the current session is able to submit, by sesing if their answer has been approved
        """
        return True

