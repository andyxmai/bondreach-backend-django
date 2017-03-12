from django.conf.urls import url, include
from contact.api.v1 import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'contacts', api.ContactViewSet, base_name='contact')
router.register(r'follow-ups', api.FollowUpViewSet, base_name='follow-up')

urlpatterns = [
  url(r'^', include(router.urls)),
]