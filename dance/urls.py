from django.conf.urls import re_path
from django.urls import include

from . import views


urlpatterns = [
    re_path(r'^$', views.list_steps),
    re_path(r'^artist/(?P<artist_id>[0-9]+)/$', views.artist_detail, name='artist_detail'),
    re_path(r'^step/(?P<step_id>[0-9]+)/$', views.step_detail, name='step_detail'),
    re_path(r'^video/(?P<video_id>[0-9]+)/$', views.video_detail, name='video_detail'),
    re_path(r'^video/create/$', views.video_creation, name='video_creation'),
    re_path(r'^api/', include('dance.api.urls')),
    re_path(r'^search/$', views.search_step, name='search'),
]