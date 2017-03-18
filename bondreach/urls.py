"""bondreach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from region import views


urlpatterns = [
  url(r'', include('account.api.urls')),
  url(r'', include('contact.api.urls')),
  url(r'', include('customer.api.urls')),
  url(r'', include('investment.api.urls')),
  url(r'', include('region.api.urls')),
  url(r'^admin/', admin.site.urls),
  url(r'^.well-known/acme-challenge/QO5VmmdZPJa0X2NYdPaF8GplsTg2IPekQu5OpZ1mKS8', views.index, name='index'),
]
