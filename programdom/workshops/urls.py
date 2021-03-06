from django.urls import path

from programdom.workshops.views import WorkshopCreateView, WorkshopDetailView, WorkshopListView, \
    WorkshopStudentRegigsterView, WorkshopStudentWaitView, WorkshopPresentView, WorkshopEditProblemsView

urlpatterns = [
    path("auth/", WorkshopStudentRegigsterView.as_view(), name="workshop_auth"),
    path("", WorkshopListView.as_view(), name="workshop_list"),
    path("new/", WorkshopCreateView.as_view(), name="workshop_new"),
    path("<int:pk>/", WorkshopDetailView.as_view(), name="workshop_detail"),
    path("<int:pk>/waiting/", WorkshopStudentWaitView.as_view(), name="workshop_student_waiting"),
    path("<int:pk>/present/", WorkshopPresentView.as_view(), name="workshop_present"),
    path("<int:pk>/problems/", WorkshopEditProblemsView.as_view(), name="workshop_problems"),

]
