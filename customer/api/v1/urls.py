from django.conf.urls import url, include
from customer.api.v1 import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customers', api.CustomerViewSet)


urlpatterns = [
  url(r'^customers/beta/$', api.BetaList.as_view()),
  url(r'^', include(router.urls)),
]