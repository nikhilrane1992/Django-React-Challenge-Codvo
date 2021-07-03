from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from swift_lyrics import views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^lyric/$', views.APIIndex.as_view(), name='api_index'),
    url(r'^lyric/(?P<pk>\d+)/?$', views.APIDetail.as_view(), name='api_detail'),
    url(r'^lyric/(?P<pk>\d+)/(?P<vote_type>[\w\-]+)/?$', views.LyricUpvoteDownVote.as_view(), name='api_upvote_downvote'),
    url(r'^lyric-random/?$', views.RandomLyric.as_view(), name='api_random_lyric'),
    url(r'^album/$', views.AlbumIndex.as_view(), name='album_index'),
    url(r'^album/(?P<pk>\d+)/?$', views.AlbumDetail.as_view(), name='album_detail'),
    url(r'^song/$', views.SongIndex.as_view(), name='song_index'),
    url(r'^song/(?P<pk>\d+)/?$', views.SongDetail.as_view(), name='song_detail'),
    url(r'^artist/$', views.ArtistIndex.as_view(), name='artist_index'),
    url(r'^artist/(?P<pk>\d+)/?$', views.ArtistDetail.as_view(), name='artist_detail'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
