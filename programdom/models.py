import random
import string

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse

User = get_user_model()


class Problem(models.Model):
    """
    A single problem
    """
    mooshak_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    skeleton = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class WorkshopSession(models.Model):
    """
    A workshop is a single session
    """
    code = models.CharField(max_length=8, null=True, blank=True)
    problems = models.ManyToManyField(Problem, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def active(self):
        return self.code is not None

    def end(self):
        """s
        Ends the session, by removing the session code
        """
        self.code = None
        self.save()

    def start(self):
        """
        Sets the session as running, by setting a code
        """
        self.code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.save()

    def get_absolute_url(self):
        return reverse('workshop_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.title


class Submission(models.Model):
    """
    A users submission of code for a problem
    """
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.FileField()
    options = JSONField(blank=True, default=dict)


class SubmissionResult(models.Model):
    """
    The result of a Submission after it has been testsed
    """
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
    result_data = JSONField(blank=True, default=dict)
    std_out = models.FileField()
    std_err = models.FileField()
    