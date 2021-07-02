from django.contrib import admin

# Register your models here.
from swift_lyrics.models import Lyric, Song, Album, Artist

admin.site.register(Lyric)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Artist)
