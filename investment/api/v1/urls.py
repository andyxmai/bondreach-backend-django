from django.conf.urls import url, include
from investment.api.v1 import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'investment-types', api.InvestmentTypeViewSet)

urlpatterns = [
  url(r'^', include(router.urls)),
]