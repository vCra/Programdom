from django.urls import path

from programdom.workshops.views import WorkshopCreateView, WorkshopDetailView, WorkshopListView

urlpatterns = [
    path("", WorkshopListView.as_view(), name="workshop_list"),
    path("new/", WorkshopCreateView.as_view(), name="workshop_new"),
    path("<int:pk>/", WorkshopDetailView.as_view(), name="workshop_detail")

]
