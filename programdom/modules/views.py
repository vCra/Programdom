from django.views.generic import TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin, ListView

from programdom.models import Module


class MyModulesView(ListView):
    model = Module


class ModuleDetailView(DetailView):
    model = Module

    def get_object(self, queryset=None):
        return (queryset or self.get_queryset()).get(code=self.kwargs.get("code"))
