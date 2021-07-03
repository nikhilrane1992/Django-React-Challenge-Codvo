from drf_yasg import openapi
from rest_framework import serializers
from random import randint
from django.db.models.aggregates import Count
from swift_lyrics.models import Lyric, Song, Album, Artist


class BaseArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'first_year_active']
        

class BaseAlbumSerializer(serializers.ModelSerializer):
    artist = BaseArtistSerializer()

    def validate(self, data):
        artist_id = self.initial_data.get('artist', dict()).get('id', None)
        if artist_id:
            # If song_id, then the album and song already exist, just fetch them from datastore
            artist_obj = Artist.objects.filter(id=artist_id).first()
            if not artist_obj:
                error = {'message': 'Artist with id %s not available in database, Please enter valid artist id' % artist_id}
                raise serializers.ValidationError(error)
            data['artist'] = artist_obj
        else:
            error = {'message': 'Pass artist id in API body request'}
            raise serializers.ValidationError(error)
        return super().validate(data)

    def create(self, validated_data):
        album = Album(**validated_data)
        album.save()    
        return album

    class Meta:
        model = Album
        fields = ['id', 'name', 'year'] + ['artist']


class ArtistAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['id', 'name', 'year'] 


class ArtistDetailSerializer(BaseArtistSerializer):
    albums = ArtistAlbumSerializer(many=True, read_only=True)

    class Meta(BaseArtistSerializer.Meta):
        fields = BaseArtistSerializer.Meta.fields + ['albums']


class BaseSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ['id', 'name']


class LyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ['id', 'text', 'upvotes', 'downvotes']


class AlbumDetailSerializer(BaseAlbumSerializer):
    songs = BaseSongSerializer(many=True, read_only=True)

    class Meta(BaseAlbumSerializer.Meta):
        fields = BaseAlbumSerializer.Meta.fields + ['songs']

    def create(self, validated_data):
        album = Album(**validated_data)
        album.save()    
        return album


class SongSerializer(BaseSongSerializer):
    album = BaseAlbumSerializer()

    class Meta(BaseSongSerializer.Meta):
        fields = BaseSongSerializer.Meta.fields + ['album']

class SongDetailSerializer(SongSerializer):
    lyrics = LyricSerializer(many=True, read_only=True)

    class Meta(SongSerializer.Meta):
        fields = SongSerializer.Meta.fields + ['lyrics']


class LyricDetailSerializer(LyricSerializer):
    song = BaseSongSerializer(read_only=True)
    album = BaseAlbumSerializer(source='song.album', read_only=True)

    def validate(self, data):
        song_id = self.initial_data.get('song', dict()).get('id', None)
        if song_id:
            # If song_id, then the album and song already exist, just fetch them from datastore
            song = Song.objects.get(id=song_id)
            data['song'] = song
        else:
            # If album_id, then album already exists - just fetch, then handle create/fetch song
            album_id = self.initial_data.get('album', dict()).get('id', None)

            song = self.initial_data.get('song', dict())
            song_name = song.get('name', None)

            album = None
            if album_id:
                album = Album.objects.filter(id=album_id).first()
                if not album:
                    error = {'message': 'Album with id %s not available in database, Please enter valid album id' % album_id}
                    raise serializers.ValidationError(error)
            else:
                error = {'message': 'Pass album id in API body request'}
                raise serializers.ValidationError(error)

            if song_name:
                song = Song.objects.filter(name=song_name).first()
                if song is None:
                    song = Song(name=song_name, album=album)
                    song.save()
                data['song'] = song

        return super().validate(data)

    def create(self, validated_data):
        lyric = Lyric(**validated_data)
        lyric.save()    
        return lyric

    class Meta(LyricSerializer.Meta):
        fields = LyricSerializer.Meta.fields + ['song', 'album']


class LyricVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ['id', 'upvotes', 'downvotes']

    def update(self, instance, validation_data):
        """
        Update and return an existing lyric instance, given upvote or donvote.
        """
        vote_type = self.context.get('view').kwargs.get('vote_type')
        if vote_type == 'upvote':
            instance.upvotes = instance.upvotes + 1
        elif vote_type == 'downvote':
            instance.downvotes = instance.downvotes - 1
        else:
            error = {'message': 'Vote type value %s is not valid, Proper value is (upvote/downvote)' % vote_type}
            raise serializers.ValidationError(error)
        instance.save()
        return instance


class LyricRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ['id', 'text', 'upvotes', 'downvotes']

