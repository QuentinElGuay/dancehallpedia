from rest_framework import viewsets

from pages.models import Artist
from .serializers import ArtistPostSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artists to be viewed or edited.
    """
    queryset = Artist.objects.all().order_by('name')
    serializer_class = ArtistPostSerializer
