from django.urls import path, include


urlpatterns = [
    path("workshops/", include("programdom.workshops.urls")),
    path("problems/", include("programdom.problems.urls")),
    path("api/", include("programdom.api.routes"))
]
