from django.urls import path
from django.views import View

from programdom.problems.views import ProblemStudentView

urlpatterns = [
    path("", View.as_view(), name="problem_base"),
    path("<int:pk>/", ProblemStudentView.as_view(), name="problem_student"),
    path("new/", ProblemStudentView.as_view(), name="problem_new"),
]
