from django.conf.urls import url, include
from customer.api.v1 import api

urlpatterns = [
  url(r'^customers/beta/$', api.BetaList.as_view()),  
]