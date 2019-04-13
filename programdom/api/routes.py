from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'submissions', views.SubmissionView)
router.register(r'problems', views.ProblemView)


urlpatterns = [
    path('', include((router.urls, "programdom"), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
