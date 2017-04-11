from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('event.api.v1.urls')),
]