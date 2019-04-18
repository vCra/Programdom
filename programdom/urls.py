from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("workshops/", include("programdom.workshops.urls")),
    path("problems/", include("programdom.problems.urls")),
    path("api/", include("programdom.api.routes")),
]
