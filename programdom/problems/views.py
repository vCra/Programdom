from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView

from programdom.models import Problem
from programdom.problems.forms import EditProblemForm


class ProblemListView(ListView):
    model = Problem
    template_name = "programdom/problem/problem_list.html"


class ProblemStudentView(DetailView):

    model = Problem
    template_name = "programdom/problem/student.html"


class ProblemDetailView(SuccessMessageMixin, UpdateView):
    model = Problem
    template_name = "programdom/problem/problem_detail_view.html"
    form_class = EditProblemForm
    success_message = "Problem Details have been successfully Updated!"


class ProblemDeleteView(DeleteView):
    model = Problem
    template_name = "programdom/problem/problem_delete.html"
    success_url = reverse_lazy('problem_list')


class ProblemCreateView(CreateView):
    model = Problem
    template_name = "programdom/problem/problem_create.html"
    form_class = EditProblemForm
