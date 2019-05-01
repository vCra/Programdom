from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve, reverse


class LoginRequiredMiddleware:
    """
    Middlewear to ensure that the current "user" is allowed to complete the current request

    The system currently checks if the user is authenticated or if they have a "current_workshop_id"

    Unauthenticated/unauthorised users are sent to the login page
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.student_views = settings.STUDENT_VIEWS
        self.open_urls = [self.login_url] + \
                         getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):

        if request.user.is_authenticated:
            return self.get_response(request)
        elif request.session.get("current_workshop_id"):
            if self._is_student_url(request.path_info):
                return self.get_response(request)
            else:
                messages.error(request, "You need to be logged in to view this page")
                return redirect(reverse("users:login"))
        elif request.path_info in self.open_urls:
            return self.get_response(request)
        else:
            return redirect(self.login_url+'?next='+request.path)



        # if not (request.user.is_authenticated or request.session.get("current_workshop_id")) and not (request.path_info in self.open_urls or request.path_info.startswith("/static/")):
        #     return redirect(self.login_url+'?next='+request.path)
        # else:
        #     if request.session.get("current_workshop_id") and not self._is_student_url(request.path_info):
        #         return redirect(reverse("users:login"))
        # return self.get_response(request)

    def _is_student_url(self, path):
        return resolve(path).view_name in self.student_views