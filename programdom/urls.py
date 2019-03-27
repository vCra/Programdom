from django.urls import path, include

from programdom.problems.views import ProblemStudentView

urlpatterns = [
    path("workshops/", include("programdom.workshops.urls")),
    path("problems/", include("programdom.problems.urls")),
    path("api/", include("programdom.api.routes")),

    path("student/<int:pk>/", ProblemStudentView.as_view, name="student_view")
]
