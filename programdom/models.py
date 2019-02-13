from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField


User = get_user_model()



class Module(Group):
    """
    A Module, extends from a django group for ease of use
    """
    code = models.CharField(max_length=8)
    coordinatior = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Workshop(models.Model):
    """
    A workshop is a single session for a module. It can have multiple problems within it, and can have time data so that
    students can quickly go to in progress workshops
    """
    title = models.CharField(max_length=255, null=True)
    time = DateTimeRangeField(null=True)


class Problem(models.Model):
    """
    A single problem that is part of an assignment
    """
    workshops = models.ManyToManyField(Workshop)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    options = JSONField(blank=True, default="{}")


class Submission(models.Model):
    """
    A users submission of code for a problem
    """
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.FileField()
    options = JSONField(blank=True, default="{}")


class SubmissionResult(models.Model):
    """
    The result of a Submission after it has been testsed
    """
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
    result_data = JSONField(blank=True, default="{}")
    std_out = models.FileField()
    std_err = models.FileField()
    