from rest_framework import mixins, generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from random import randint
from django.db.models.aggregates import Count
from rest_framework.decorators import action

from django.http import HttpResponse
from django.views import View
# Create your views here.
from swift_lyrics.models import Lyric, Album, Song, Artist
from swift_lyrics.serializers.serializer import LyricSerializer, BaseSongSerializer, BaseAlbumSerializer, \
    AlbumDetailSerializer, \
    SongDetailSerializer, LyricSerializer, SongSerializer, \
    LyricDetailSerializer, LyricVotesSerializer, \
    BaseArtistSerializer, ArtistDetailSerializer, LyricRandomSerializer


class HealthCheckView(View):
    """
    Checks to see if the site is healthy.
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")


class AlbumIndex(mixins.ListModelMixin,
                 generics.GenericAPIView,
                 mixins.CreateModelMixin):
    serializer_class = BaseAlbumSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AlbumDetail(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = AlbumDetailSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SongIndex(mixins.ListModelMixin,
                 generics.GenericAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SongDetail(mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = SongDetailSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class APIIndex(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    serializer_class = LyricDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'song__name', 'song__album__name']
    ordering_fields = ['text', 'song__name', 'song__album__name']


    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class APIDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LyricUpvoteDownVote(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = LyricVotesSerializer

    def get_queryset(self):
        return Lyric.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RandomLyric(generics.GenericAPIView,
                mixins.ListModelMixin):
    serializer_class = LyricRandomSerializer
    pagination_class = None

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        count = Lyric.objects.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        data = Lyric.objects.all()[random_index]

        serializer = self.get_serializer(data)
        return Response(serializer.data)


class ArtistIndex(mixins.ListModelMixin,
                 generics.GenericAPIView,
                 mixins.CreateModelMixin):
    serializer_class = BaseArtistSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'first_year_active']
    ordering_fields = ['first_year_active', 'name']
    filterset_fields = {
        'first_year_active':['gt', 'lt'],
    }

    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArtistDetail(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                generics.GenericAPIView):
    serializer_class = ArtistDetailSerializer
    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
