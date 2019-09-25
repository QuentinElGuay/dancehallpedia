from rest_framework import serializers

from pages.models import Artist


class ArtistPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ['pk', 'name']
