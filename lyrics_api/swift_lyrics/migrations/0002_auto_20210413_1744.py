# Generated by Django 3.2 on 2021-04-13 17:44

from django.db import migrations, models
import django.db.models.deletion
import json

from swift_lyrics.models import Lyric, Album, Song


def load_initial_data(apps, schema_editor):
    json_data = open('swift_lyrics/fixtures/quotes.json')
    data = json.load(json_data)
    for d in data:
        album_name = d['album']
        song_name = d['song']
        text = d['quote']

        album = Album.objects.filter(name=album_name).first()
        if album is None:
            album = Album(name=album_name)
            album.save()

        song = Song.objects.filter(name=song_name).first()
        if song is None:
            song = Song(name=song_name, album=album)
            song.save()

        Lyric(song=song, text=text).save()
    
    json_data.close()


class Migration(migrations.Migration):

    dependencies = [
        ('swift_lyrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, help_text='Artist name', unique=True)),
                ('first_year_active', models.IntegerField(blank=True, help_text='First Year Active')),
            ],
        ),
        migrations.RenameField(
            model_name='lyric',
            old_name='votes',
            new_name='downvotes',
        ),
        migrations.AddField(
            model_name='album',
            name='year',
            field=models.IntegerField(help_text='Album year', null=True),
        ),
        migrations.AddField(
            model_name='lyric',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(help_text='Artist', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='swift_lyrics.artist'),
        ),  
        migrations.RunPython(load_initial_data)
    ]
