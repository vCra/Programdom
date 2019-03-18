from rest_framework import serializers

from programdom.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'problem', 'user', 'code', 'options')

