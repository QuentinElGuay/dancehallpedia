from rest_framework import serializers

from dance.models import Artist, Step, Tag, Video, StepAppearance, AlternativeStepName


class ArtistPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ['pk', 'name']


class StepAppearanceSerializer(serializers.ModelSerializer):
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all().order_by('title'))
    step = serializers.PrimaryKeyRelatedField(queryset=Step.objects.all().order_by('name'))

    class Meta:
        model = StepAppearance
        fields = ['pk', 'time', 'video', 'step']


class StepSerializer(serializers.ModelSerializer):
    video = StepAppearanceSerializer(read_only=True, many=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), allow_null=True)

    class Meta:
        model = Step
        fields = ['pk', 'name', 'creator', 'school', 'created_at', 'video']


class AlternativeStepNameSerializer(serializers.HyperlinkedModelSerializer):
    step = serializers.PrimaryKeyRelatedField(queryset=Step.objects.all().order_by('name'), allow_null=True)

    class Meta:
        model = AlternativeStepName
        fields = ['pk', 'step', 'value']


class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['pk', 'name']


class VideoPostSerializer(serializers.HyperlinkedModelSerializer):
    step = StepAppearanceSerializer(read_only=True, many=True)

    class Meta:
        model = Video
        fields = ['pk', 'url', 'title', 'channel', 'channel_url', 'valid', 'host', 'type', 'step']
