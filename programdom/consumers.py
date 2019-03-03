import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class StudentWaitingConsumer(WebsocketConsumer):

    workshop_code = None

    def connect(self):
        """
        Called when a connection is attempted
        :return:
        """
        session = self.scope["session"]
        self.workshop_code = session.get("current_workshop_id", None)
        if self.workshop_code:

            # Add this consumer to the wait_workshop_* group, so we know when the workshop starts
            async_to_sync(self.channel_layer.group_add)(
                f"wait_workshop_{self.workshop_code}", self.channel_name
            )

            self.accept()
        else:
            # If they is no workshop code, close the connection
            logging.getLogger(__name__).warning("A connection was initiated, but no workshop ID was present within the users session")
            self.close()

    def problem_ready(self, event):
        """
        Send a message to the user, telling them to load up a problem. The JS on the client side will handle redirection
        :return:
        """
        problem = event["problem"]

        self.send(text_data=json.dumps({
            "problem": problem
        }))

class WorkshopControlConsumer(WebsocketConsumer):

    def connect(self):
        """
        Called when a connection is attempted
        :return:
        """
        session = self.scope["session"]
        # TODO: Check if this Account is actually allowed to interact with this workshop

        self.workshop_code = session.get("current_workshop_id", None)
        if self.workshop_code:
            self.accept()
        else:
            # If they is no workshop code, close the connection
            logging.getLogger(__name__).warning("A connection was initiated, but no workshop ID was present within the users session")
            self.close()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message_type = text_data["action"]
        try:
            getattr(self, message_type)(text_data)
        except Exception as e:
            print(e)

    def change_problem(self, text_data: dict):
        async_to_sync(self.channel_layer.group_send)(f"wait_workshop_{self.workshop_code}", {"type": "problem.ready", "problem": text_data.get("problem_id")})
        print("test")
