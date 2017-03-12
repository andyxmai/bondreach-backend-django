from django.conf.urls import url, include
from region.api.v1 import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'regions', api.RegionViewSet)

urlpatterns = [
  url(r'^', include(router.urls)),
]