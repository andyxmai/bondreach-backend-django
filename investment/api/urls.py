from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('investment.api.v1.urls')),
]