from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('region.api.v1.urls')),
]