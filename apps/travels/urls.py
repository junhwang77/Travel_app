from django.conf.urls import url, include
from . import views
#from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name = 'destination'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^create$', views.create, name = 'create'),
    url(r'^join$', views.join, name = 'join'),
    url(r'^remove$', views.remove, name = 'remove'),
]
