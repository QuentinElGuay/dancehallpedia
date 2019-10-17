from django.conf.urls import re_path
from django.urls import include

from . import views


urlpatterns = [
    re_path(r'^$', views.list_steps),
    re_path(r'^step/(?P<step_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^api/', include('dance.api.urls')),
]