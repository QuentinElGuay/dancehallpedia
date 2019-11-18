from django.db.models import Value, IntegerField
from django.contrib.postgres.search import TrigramSimilarity
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dance.models import Artist, Step, Tag, Video, StepAppearance, AlternativeStepName
from .serializers import ArtistPostSerializer, StepSerializer, TagPostSerializer, VideoPostSerializer, \
    StepAppearanceSerializer, AlternativeStepNameSerializer


class ArtistFilter(filters.FilterSet):
    class Meta:
        model = Artist
        fields = {
            'name': ['icontains', 'iexact'],
        }


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artists to be viewed or edited.
    """
    queryset = Artist.objects.all().order_by('name')
    serializer_class = ArtistPostSerializer
    filterset_class = ArtistFilter

    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        artist_steps = Step.objects.filter(creator__pk=pk).order_by('name')

        page = self.paginate_queryset(artist_steps)
        if page is not None:
            serializer = StepSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StepSerializer(artist_steps, many=True)
        return Response(serializer.data)


class AlternativeStepNameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AlternativeStepNames to be viewed or edited.
    """
    queryset = AlternativeStepName.objects.all().order_by('value')
    serializer_class = AlternativeStepNameSerializer
    filter_fields = ('step', 'value')


class StepAppearanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stepsAppearance to be viewed or edited.
    """
    queryset = StepAppearance.objects.all().order_by('pk')
    serializer_class = StepAppearanceSerializer
    filter_fields = ('step', 'video', 'time')


class StepFilter(filters.FilterSet):
    class Meta:
        model = Step
        fields = {
            'name': ['icontains', 'iexact'],
        }


class StepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows steps to be viewed or edited.
    """
    queryset = Step.objects.all().order_by('name')
    serializer_class = StepSerializer
    filterset_class = StepFilter

    @action(detail=False, url_path='search/(?P<step_name>[^/.]+)')
    def search(self, request, step_name=None):
        """
        API endpoint that allows fuzzy matching on step name.
        """
        fuzzy_matching_steps = Step.objects.annotate(similarity=TrigramSimilarity('name', step_name),
                                                     ).filter(similarity__gt=0.3).order_by('-similarity')

        contains_matching_steps = Step.objects.filter(name__icontains=step_name)

        possible_steps = fuzzy_matching_steps | contains_matching_steps

        page = self.paginate_queryset(possible_steps)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(possible_steps, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagPostSerializer


class VideoFilter(filters.FilterSet):
    class Meta:
        model = Video
        fields = {
            'url': ['iexact'],
            'title': ['icontains', 'iexact'],
            'channel': ['icontains', 'iexact'],
        }


class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be viewed or edited.
    """
    queryset = Video.objects.all().order_by('title')
    serializer_class = VideoPostSerializer
    filterset_class = VideoFilter
