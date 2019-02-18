from django.urls import path

from programdom.modules.views import MyModulesView, ModuleDetailView, ModuleCreateView, ModuleEditUsersView

urlpatterns = [
    path("", MyModulesView.as_view(), name="module_list"),
    path("new/", ModuleCreateView.as_view(), name="module_new"),
    path("<code>/", ModuleDetailView.as_view(), name="module_detail"),
    path("<code>/users/update", ModuleEditUsersView.as_view(), name="module_users_update"),
]
