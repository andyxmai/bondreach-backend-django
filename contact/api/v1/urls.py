from django.conf.urls import url, include
from contact.api.v1 import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'contacts', api.ContactViewSet, base_name='contact')
router.register(r'contacts-downloads', api.DownloadContactViewSet, base_name='contacts-downloads')
router.register(r'follow-ups', api.FollowUpViewSet, base_name='follow-up')
router.register(r'correspondences', api.CorrespondenceViewSet, base_name='correspondence')

urlpatterns = [
  url(r'^', include(router.urls)),
]