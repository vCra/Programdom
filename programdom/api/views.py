from rest_framework import viewsets
from .serializers import SubmissionSerializer, ProblemSerializer
from programdom.models import Submission, Problem


class SubmissionView(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class ProblemView(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
