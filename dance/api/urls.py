from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import ArtistViewSet, StepViewSet, StepAppearanceViewSet, TagViewSet, VideoViewSet, AlternativeStepNameViewSet

router = DefaultRouter()
router.register(r'artist', ArtistViewSet)
router.register(r'alternativeStepName', AlternativeStepNameViewSet)
router.register(r'step', StepViewSet)
router.register(r'stepAppearance', StepAppearanceViewSet)
router.register(r'tag', TagViewSet)
router.register(r'video', VideoViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]
