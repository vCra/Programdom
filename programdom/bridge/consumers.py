import aiofiles as aiofiles
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from django.core.cache import cache

from channels.layers import get_channel_layer
from django.conf import settings
import mooshak2api as api

from programdom.bridge.client import client

channel_layer = get_channel_layer()


class ProgramdomBridgeConsumer(AsyncConsumer):

    async def evaluate(self, message):
        """
        Sends a message to mooshak, and then processes the result
        :param message: a dict containing the following:
            message = {
                "type": "solution.evaluate", # To match to this method
                "problem_id": The Mooshak ID of the problem this solution is for
                "code_url": The URL of the code for this submission
                "session_id": The clients session_id - used to send messages back to the user
                "workshop_id": the PK of the workshop associated with this submission - used for stats tracking
            }
        """

        problem = await sync_to_async(api.problems.Problem)(settings.MOOSHAK_CONTEST)
        problem.id = message["problem_id"]

        url = message["code_url"]


        # Our old system downloaded files and then sent them off. We will probably go back to this once in prod and have
        # an actual object storage system working. However, ATM we can just use the local files.

        # async with aiohttp.ClientSession() as session:
        #     # TODO: Check file is accessable (aka http 200)
        #     async with session.get(f"{url}") as response:
        #         data = await response.read()

        # We can just get the file
        try:
            # TODO: This is horrible, and should be changed
            async with aiofiles.open(str(settings.APPS_DIR(url[1:])), mode='rb') as f:
                self.evaluation = await sync_to_async(problem.evaluate)(client, await f.read())

        except Exception as e:
            message.update({
                "notif_type": "error",
                "message": str(e)
            })
        else:
            message.update({
                "notif_type": self.evaluation.notify_type,
                "message": self.evaluation.as_json(),
            })
        message.update({"type":"submission.status"})
        channel_name = await cache.get(f"session_{message['session_id']}_channel-name")
        await channel_layer.send(channel_name, message)

        status = await cache.get(f"session_{message['session_id']}_status")
        notify_type = message["notif_type"]

        #TODO: Sort this mess out - make some form of cache object class IDK
        if status == "not_attempted":
            if notify_type == "success":
                cache.incr(f"workshop_{message['workshop_id']}_users_passed")
                new_status = cache.set(f"session_{message['session_id']}_status", "success")
            else:
                cache.incr(f"workshop_{message['workshop_id']}_users_attempted")
                new_status = cache.set(f"session_{message['session_id']}_status", "attempted")
            cache.set(f"session_{message['session_id']}_status", new_status)
        elif status == "attempted":
            if notify_type == "success":
                cache.incr(f"workshop_{message['workshop_id']}_users_passed")
                new_status = cache.set(f"session_{message['session_id']}_status", "success")
                cache.set(f"session_{message['session_id']}_status", new_status)

        await channel_layer.group_send(f"workshop_{message['workshop_id']}_control", {"type": "graph.update"})
