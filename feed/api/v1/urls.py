from django.conf.urls import url, include
from feed.api.v1 import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'news-feed', api.NewsFeedViewSet, base_name='news-feed')

urlpatterns = [
  url(r'^', include(router.urls)),
]