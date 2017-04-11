from django.conf.urls import url, include
from event.api.v1 import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'team-events', api.TeamEventViewSet, base_name='team-events')

urlpatterns = [
  url(r'^', include(router.urls)),
]