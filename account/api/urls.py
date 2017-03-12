from django.conf.urls import url, include

urlpatterns = [
  url('^v1/', include('account.api.v1.urls')),

]