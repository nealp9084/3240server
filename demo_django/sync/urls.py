from django.conf.urls import patterns, url

from sync import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create_server_file/$', views.create_server_file, name='create_server_file'),
    url(r'^(?P<file_id>\d+)/update_file/$', views.update_file, name='update_file'),
    url(r'^(?P<file_id>\d+)/serve_file/$', views.serve_file, name='serve_file'),
    url(r'^(?P<file_id>\d+)/delete_file/$', views.delete_file, name='delete_file'),
    url(r'^show_history/$', views.show_history, name='show_history')
)
