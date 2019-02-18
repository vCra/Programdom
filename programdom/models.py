from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
from django.urls import reverse

User = get_user_model()


class Module(models.Model):
    """
    A Module, extends from a django group for ease of use
    """
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="modules")
    code = models.CharField(max_length=8)
    coordinatior = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="modules_taught")

    def get_absolute_url(self):
        return reverse('module_detail', kwargs={'code': self.code})

    def __str__(self):
        return self.name


class Workshop(models.Model):
    """
    A workshop is a single session for a module. It can have multiple problems within it, and can have time data so that
    students can quickly go to in progress workshops
    """
    title = models.CharField(max_length=255, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    modules = models.ManyToManyField(Module)

    def get_absolute_url(self):
        return reverse('workshop_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.title


class Problem(models.Model):
    """
    A single problem that is part of an assignment
    """
    workshops = models.ManyToManyField(Workshop)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    options = JSONField(blank=True, default=dict)


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
    