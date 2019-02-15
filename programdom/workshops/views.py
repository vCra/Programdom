from django.views.generic import DetailView

from programdom.models import Workshop


class WorkshopDetailView(DetailView):
    model = Workshop

    def get_object(self, queryset=None):
        return queryset.get(code=self.kwargs.get("code"))