from django.urls import path

from programdom.problems.views import ProblemStudentView, ProblemListView, ProblemDetailView, ProblemDeleteView, \
    ProblemCreateView, ProblemTestcaseCreateView, ProblemTestCaseUpdateView, ProblemTestCaseDeleteView

urlpatterns = [
    path("", ProblemListView.as_view(), name="problem_list"),
    path("new/", ProblemCreateView.as_view(), name="problem_create"),
    path("<int:pk>/", ProblemDetailView.as_view(), name="problem_detail"),
    path("<int:pk>/delete/", ProblemDeleteView.as_view(), name="problem_delete"),
    path("<int:pk>/student/", ProblemStudentView.as_view(), name="problem_student"),
    path("<int:pk>/tests/new/", ProblemTestcaseCreateView.as_view(), name="problem_test_new"),
    path("<int:pk>/tests/<int:tc_pk>/", ProblemTestCaseUpdateView.as_view(), name="problem_test_update"),
    path("<int:pk>/tests/<int:tc_pk>/delete/", ProblemTestCaseDeleteView.as_view(), name="problem_test_delete"),



]
