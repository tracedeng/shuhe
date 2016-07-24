"""shuhe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from shuhe.views import test
#from books.views import contact
from market import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/', test),
    url(r'^p/ge/$', views.appliances),
    url(r'^p/lg/$', views.lifegear),
    url(r'^p/lg/([A-Za-z0-9]+)/$', views.lifegear_sub),
    url(r'^ma$', views.maintenance_apply),
    url(r'^m$', views.maintenance),
    url(r'^city$', views.cities),
    url(r'^county$', views.counties),
    url(r'^o', views.order),
    url(r'^po', views.place_order),
    url(r'^pay', views.pay),
    url(r'^notice', views.pay_notice),
    url(r'^$', views.index),
]

