from rest_framework import serializers
from programdom.models import Submission, Problem


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'problem', 'user', 'code', 'workshop', 'options')


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'title', 'skeleton', 'language')