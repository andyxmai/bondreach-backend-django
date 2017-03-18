from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('customer.api.v1.urls')),
]