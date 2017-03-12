from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('contact.api.v1.urls')),
]