from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin

from programdom.models import Workshop
from programdom.workshops.Forms import WorkshopsForm
from programdom.workshops.tables import WorkshopTable


class WorkshopDetailView(DetailView):
    model = Workshop


class WorkshopCreateView(SuccessMessageMixin, CreateView):
    model = Workshop
    form_class = WorkshopsForm
    success_message = "A new Workshop has been created successfully! Remember to assign it to any modules"


class WorkshopListView(SingleTableMixin, FilterView):
    model = Workshop
    table_class = WorkshopTable
    template_name = "programdom/workshop_list.html"
