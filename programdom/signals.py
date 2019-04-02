from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from programdom.models import Submission


channel_layer = get_channel_layer()

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

    async_to_sync(channel_layer.send)(
        "mooshakbridge", {
            "type": "evaluate",
            "problem_id": instance.problem.id,
            "code_url": instance.code.url,
            "session_id": instance.options["session_id"],
            "workshop_id": instance.options["workshop_id"],
        }
    )
    print("test1")


