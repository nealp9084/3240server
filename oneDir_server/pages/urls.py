from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from pages import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^get_client/$', views.get_client, name='get_client'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^admin_show_users/$', views.admin_show_users, name='admin_show_users'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^admin_change_password/$', views.admin_change_password, name='admin_change_password'),
    url(r'^delete_user/$', views.delete_user, name='delete_user'),
    url(r'^admin_delete_user/$', views.admin_delete_user, name='admin_delete_user'),
    url(r'^show_history/$', views.show_history, name='show_history'),
    url(r'^admin_show_history/$', views.admin_show_history, name='admin_show_history'),
    url(r'^show_files/$', views.show_files, name='show_files'),
    url(r'^admin_show_files/$', views.admin_show_files, name='admin_show_files'),
)
