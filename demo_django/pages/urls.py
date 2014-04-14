from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from pages import views

urlpatterns = patterns('',
    # url(r'^create_user$', TemplateView.as_view(template_name='create_user.html'), name='create_user'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^get_client/$', views.get_client, name='get_client'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^delete_user/$', views.delete_user, name='delete_user'),
    url(r'^show_history/$', views.show_history, name='show_history'),
)
