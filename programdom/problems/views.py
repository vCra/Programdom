from django.views.generic import DetailView

from programdom.models import Problem


class ProblemStudentView(DetailView):
    model = Problem
    template_name = "programdom/problem/student.html"
