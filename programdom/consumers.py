import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.core.cache import cache

from programdom.models import WorkshopSession


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


class StudentWorkshopConsumer(JsonWebsocketConsumer):
    workshop_code = None
    session = None

    def connect(self):
        """
        Called when a connection is attempted to this consumer
        :return:
        """
        self.session = self.scope["session"]
        self.workshop_code = self.session.get("current_workshop_id", None)
        if self.workshop_code:

            # Add this consumer to the wait_workshop_* group, so we know when the workshop starts
            async_to_sync(self.channel_layer.group_add)(
                f"wait_workshop_{self.workshop_code}", self.channel_name
            )

            # Add a mapping between this consumer and the session ID, to make it easier to send messages to
            cache.set(f"session_{self.session.session_key}_channel-name", self.channel_name)

            # Add 1 to the number of students connected
            cache.incr(f'workshop_{self.workshop_code}_users_count')
            async_to_sync(self.channel_layer.group_send)(f"workshop_{self.workshop_code}_control", {"type": "graph.update"})

            self.accept()
        else:
            # If they is no workshop code, close the connection
            logging.getLogger(__name__).warning("A connection was initiated, but no workshop ID was present within the users session")
            self.close()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            f"wait_workshop_{self.workshop_code}", self.channel_name
        )
        cache.delete(f"session_{self.session}_channel-name")

        # -1 to no of students connected
        cache.decr(f'workshop_{self.workshop_code}_users_count')
        async_to_sync(self.channel_layer.group_send)(f"workshop_{self.workshop_code}_control", {"type": "graph.update"})


    def problem_ready(self, event):
        """
        Send a message to the user, telling them to load up a problem.
         The JS on the client side will handle redirection
        """
        self.send_json(event)

    def submission_status(self, event):
        """
        Send a message to the user, with the details from the submission.
        This will probably be called from:
             - the save_submission signal from a submission returning a result (or error)
             - a queued task for a submission returning a result
        :param event: JSON event
        """
        self.send_json(event)


class WorkshopControlConsumer(WebsocketConsumer):

    workshop_id = None

    def connect(self):
        """
        Called when a connection is attempted
        :return:
        """
        # TODO: Check if this Account is actually allowed to interact with this workshop
        self.workshop_id = self.scope['url_route']['kwargs']['id']

        if self.workshop_id:
            async_to_sync(self.channel_layer.group_add)(
                f"workshop_{self.workshop_id}_control", self.channel_name
            )
            self.accept()
            self.graph_update(None)
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

    def problem_select(self, text_data: dict):
        problem = text_data.get("problem_id")
        try:
            cache.set(f'workshop_{self.workshop_id}_current_problem', problem)
            async_to_sync(self.channel_layer.group_send)(f"wait_workshop_{self.workshop_id}", {"type": "problem.ready", "problem": problem})
        except Exception as e:
            print(e)

    def workshop_toggle(self, text_data: dict):
        workshop_id = text_data.get("workshop_id")
        workshop = WorkshopSession.objects.get(id=workshop_id)
        # TODO: set active workshop KV
        if text_data.get("workshop_state"):
            workshop.start()
            cache.set(f'workshop_{self.workshop_id}_users_count', 0)
            cache.set(f'workshop_{self.workshop_id}_users_passed', 0)
            cache.set(f'workshop_{self.workshop_id}_users_attempted', 0)
        else:
            workshop.end()
        self.send(text_data=json.dumps(text_data))

    def graph_update(self, _):
        graph_data = {
            "action": "graph_update",
            "count": cache.get(f'workshop_{self.workshop_id}_users_count'),
            "passed": cache.get(f'workshop_{self.workshop_id}_users_passed'),
            "attempted": cache.get(f'workshop_{self.workshop_id}_users_attempted'),
        }
        self.send(text_data=json.dumps(graph_data))
