from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, FormView, TemplateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from programdom.models import WorkshopSession
from programdom.workshops.forms import WorkshopSessionEntryForm, WorkshopsForm
from programdom.workshops.tables import WorkshopTable


def get_current_problem_url(workshop_code):
    problem_id = cache.get(f'workshop_{workshop_code}_current_problem')
    if not problem_id:
        return reverse("workshop_student_waiting", kwargs={"code": workshop_code})
    return reverse("problem_student", kwargs={"pk": problem_id})


class WorkshopDetailView(DetailView):
    model = WorkshopSession
    template_name = "programdom/workshop/detail.html"


class WorkshopCreateView(SuccessMessageMixin, CreateView):
    model = WorkshopSession
    form_class = WorkshopsForm
    success_message = "A new Workshop has been created successfully! Remember to assign it to any modules"


class WorkshopListView(SingleTableMixin, FilterView):
    model = WorkshopSession
    table_class = WorkshopTable
    template_name = "programdom/workshop/workshop_list.html"


class WorkshopStudentRegigsterView(FormView):
    """
    A view that displays a workshop code entry form, and on post, checks if the code is valid (i.e. they is
    currently a workshop running which has that code. If valid, the code gets set in the users session, and
    the user will be redirected to the current session in progress
    """
    form_class = WorkshopSessionEntryForm
    template_name = "programdom/workshop/workshop_code.html"

    def form_valid(self, form):
        code = form.cleaned_data.get("code")
        self.request.session["current_workshop_id"] = code
        # TODO: Alter so we don't have to hit the DB, but still be clean
        return redirect(get_current_problem_url(code))

class WorkshopStudentWaitView(TemplateView):
    template_name = "programdom/workshop/waiting.html"