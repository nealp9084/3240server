from django.conf.urls import patterns, url

from sync import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
