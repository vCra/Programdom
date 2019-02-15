from django.urls import path

from programdom.modules.views import MyModulesView, ModuleDetailView

urlpatterns = [
    path("", MyModulesView.as_view(), name="module_list"),
    path("<code>/", ModuleDetailView.as_view(), name="module_detail")
]
