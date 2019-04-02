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

class ProblemLanguage(models.Model):
    """
    A Language that a problem can be associated with
    """
    verbose_name = models.CharField(max_length=50)
    judge_zero_id = models.PositiveIntegerField(help_text='The ID the the language within Judge0')
    mode = models.CharField(max_length=10, help_text="The 'Mode' that Ace Editor should use to format Text", null=True, blank=True)
    extension = models.CharField(max_length=10, help_text="The filename extension for this language")
    logo_name = models.CharField(max_length=20, help_text="The name of the Font Item for this language", null=True, blank=True)

    def __str__(self):
        return self.verbose_name


class Problem(models.Model):
    """
    A single problem
    """
    title = models.CharField(max_length=255, help_text="An easy to remember name for this Problem")
    skeleton = models.TextField(blank=True, default="")
    language = models.ForeignKey(ProblemLanguage, on_delete=models.CASCADE, help_text="The language that the code for this problem should be completed in")


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('problem_detail', kwargs={'pk': self.id})


class ProblemTest(models.Model):
    """
    A test for a problem.
    The STD In will get supplied to the problem, and if the STD Out of the program matches stdout, then the test
    passes
    """
    std_in = models.TextField(blank=True, default="")
    std_out = models.TextField(blank=True, default="")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)


class Workshop(models.Model):
    """
    A workshop is a single session
    """
    code = models.CharField(max_length=8, null=True, blank=True)
    problems = models.ManyToManyField(Problem, blank=True)
    title = models.CharField(max_length=255)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=~True)
    code = models.FileField()
    options = JSONField(blank=True, default=dict)


class SubmissionTestResult(models.Model):
    """
    The result of a Submission after it has been tested
    """

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    test = models.ForeignKey(ProblemTest, on_delete=models.CASCADE)
    result_data = JSONField(blank=True, default=dict)

    def add_submission_result_data(self, submission):
        self.result_data = dict(vars(submission))


