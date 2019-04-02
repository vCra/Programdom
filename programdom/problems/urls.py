from django.urls import path

from programdom.problems.views import ProblemStudentView, ProblemListView, ProblemDetailView, ProblemDeleteView, \
    ProblemCreateView

urlpatterns = [
    path("", ProblemListView.as_view(), name="problem_list"),
    path("<int:pk>/", ProblemDetailView.as_view(), name="problem_detail"),
    path("<int:pk>/delete/", ProblemDeleteView.as_view(), name="problem_delete"),
    path("new/", ProblemCreateView.as_view(), name="problem_create"),
    path("<int:pk>/student/", ProblemStudentView.as_view(), name="problem_student"),

]
