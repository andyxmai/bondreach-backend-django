from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('feed.api.v1.urls')),
]