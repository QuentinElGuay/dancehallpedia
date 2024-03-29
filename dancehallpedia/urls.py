"""dancehallpedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, re_path
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from dance import views
from dance.api.views import ArtistViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet)


urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^dance/', include(('dance.urls', 'dance'), namespace='dance')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
