from django.urls import path, include

urlpatterns = [
    path("modules/", include("programdom.modules.urls")),
]
