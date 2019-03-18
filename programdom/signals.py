from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from programdom.models import Submission

import mooshak2api as api

channel_layer = get_channel_layer()

client = api.login(
    settings.MOOSHAK_ENDPOINT,
    settings.MOOSHAK_USERNAME,
    settings.MOOSHAK_PASSWORD,
    contest=settings.MOOSHAK_CONTEST
)

@receiver(post_save, sender=Submission)
def save_submission(sender, instance, **kwargs):
    """
    Recieved after a submission is created.
    Calls the Mooshak API with the uploaded code.
    Depending on the result of the response, it will
        a. send a message to the user with the status
        b. add the mooshak submission ID to a queue, to be fetched at a later date

    :param message: a JSON string, containing:
        "type": "submission.create" - to match to this method
        "submission_id": the PK of the submission object
        "problem_id": the PK of the problem associated with this submission
        "workshop_id": the PK of the workshop associated with this submission
        "code_url": the url of the code to upload to mooshak
        "session_id": the Session ID of the user who made the submission
    """
    send_evaluation_response(instance)


def send_evaluation_response(instance):
    session_id = instance.options["session_id"]
    workshop_id = instance.options["workshop_id"]
    message = {
        "type": "submission.status",
        "problem_id": instance.problem.mooshak_id,
        "code_url": instance.code.url,
        "session_id": session_id,
        "workshop_id": workshop_id,
    }
    try:
        # TODO:
        #  We don't actually need to get the problem from Mooshak every time
        #  In the future, we can adapt the API Lib to evaluate lazily, so we can actually
        #    use api.problems.get without it hitting mooshak.
        problem = api.problems.Problem(settings.MOOSHAK_CONTEST)
        problem.id = instance.problem.mooshak_id
        evaluation = problem.evaluate(client, instance.code.file)
    except Exception as e:
        message.update({
            "notif_type": "error",
            "message": str(e)
        })
    else:
        message.update({
            "notif_type": evaluation.notify_type,
            "message": evaluation.as_json(),
        })
    channel_name = cache.get(f"session_{session_id}_channel-name")
    async_to_sync(channel_layer.send)(channel_name, message)

