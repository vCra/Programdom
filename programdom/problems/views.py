from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView

from programdom.models import Problem


class ProblemListView(ListView):
    model = Problem
    template_name = "programdom/problem/problem_list.html"


class ProblemStudentView(DetailView):
    model = Problem
    template_name = "programdom/problem/student.html"


class ProblemDetailView(UpdateView):
    model = Problem
    template_name = "programdom/problem/problem_detail_view.html"
    fields = ["title", "mooshak_id", "options"]


class ProblemDeleteView(DeleteView):
    model = Problem
    template_name = "programdom/problem/problem_delete.html"
    success_url = reverse_lazy('problem_list')

