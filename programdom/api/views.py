from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from programdom.api.serializers import SubmissionSerializer
from programdom.models import Submission


class SubmissionView(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
