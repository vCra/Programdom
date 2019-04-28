from django_filters import Filter, MultipleChoiceFilter
from django_filters.rest_framework import FilterSet
from judge0api import Judge0Status
from rest_framework import viewsets

from .serializers import SubmissionSerializer, ProblemSerializer
from programdom.models import Submission, Problem


class SubmissionFilterSet(FilterSet):
    status = MultipleChoiceFilter(
        choices=enumerate(list(Judge0Status)),
        label = "Status",
        method=lambda queryset, _, value:
        queryset.filter(submissiontestresult__result_data__status__id__in=map(int, value)).distinct()
    )

    class Meta:
        model = Submission
        fields = ['status', 'problem', 'workshop']


class SubmissionView(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filterset_class = SubmissionFilterSet


class ProblemView(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
