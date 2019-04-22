from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView

from programdom.models import Problem, ProblemTest
from programdom.problems.forms import EditProblemForm, ProblemTestForm


class ProblemListView(ListView):
    model = Problem
    template_name = "programdom/problem/problem_list.html"


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


class ProblemTestcaseCreateView(SuccessMessageMixin, CreateView):
    model = ProblemTest
    template_name = "programdom/problem/test/test_create.html"
    form_class = ProblemTestForm
    success_message = "Testcase Created Successfully"

    def get_success_url(self):
        return self.object.problem.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.problem_id = self.kwargs.get("pk")
        self.object.save()

        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(ProblemTestcaseCreateView, self).get_context_data(**kwargs)
        context.update({"parent": Problem.objects.get(id=self.kwargs.get("pk"))})
        return context


class ProblemTestCaseUpdateView(SuccessMessageMixin, UpdateView):
    model = ProblemTest
    template_name = "programdom/problem/test/test_create.html"
    form_class = ProblemTestForm
    pk_url_kwarg = "tc_pk"
    success_message = "Testcase Updated Sucessfully"

    def get_success_url(self):
        return self.object.problem.get_absolute_url()


class ProblemTestCaseDeleteView(SuccessMessageMixin, DeleteView):
    model = ProblemTest
    template_name = "programdom/problem/test/test_delete.html"
    form_class = ProblemTestForm
    pk_url_kwarg = "tc_pk"
    success_message = "Testcase Deleted Successfully"

    def get_success_url(self):
        return self.object.problem.get_absolute_url()


class ProblemStudentView(DetailView):
    model = Problem
    template_name = "programdom/problem/student.html"