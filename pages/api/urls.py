from django.conf.urls import re_path

from .views import ArtistViewSet


urlpatterns = [
    re_path(r'^(?P<pk>\d/$', ArtistViewSet, name='post-rud')
]