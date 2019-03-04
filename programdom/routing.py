from django.urls import path
from .consumers import StudentWaitingConsumer, WorkshopControlConsumer

"""
Websocket Session UrlPatterns are used for websocket connections for users which do not have a user
e.g. a student which is using a code to access
"""
websocket_urlpatterns = [
    path("waiting/", StudentWaitingConsumer),
    path("manage_workshop/<int:id>/", WorkshopControlConsumer)
]
