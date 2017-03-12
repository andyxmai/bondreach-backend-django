from django.conf.urls import url, include
from account.api.v1 import api
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token


urlpatterns = [
  url(r'^auth/outlook/$', api.OutlookAuth.as_view()),
  url(r'^auth/login/$', api.AuthLogin.as_view()),  
  url(r'^auth/api-token-verify/', verify_jwt_token),
]