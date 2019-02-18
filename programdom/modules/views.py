from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import MultipleObjectMixin, ListView

from programdom.models import Module
from programdom.modules.forms import ModuleForm, ModuleUsersForm


class MyModulesView(ListView):
    model = Module


class ModuleDetailView(DetailView):
    model = Module

    def get_object(self, queryset=None):
        return (queryset or self.get_queryset()).get(code=self.kwargs.get("code"))


class ModuleCreateView(SuccessMessageMixin, CreateView):
    model = Module
    form_class = ModuleForm
    success_message = "A new module has been created successfully!"


class ModuleEditUsersView(UpdateView):
    model = Module
    form_class = ModuleUsersForm
