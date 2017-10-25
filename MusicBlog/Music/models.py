from django.db import models


# Create your models here.
# Some of the data for the models come from the data scrapper while other
# data has to be manually filled or collected running spider/crawler and retrieve information
# from other data sources
class Album(models.Model):
    album_name = models.CharField(max_length=250)
    album_artist = models.CharField(max_length=250)
    album_songscount= models.IntegerField(default=1)
    album_logo = models.CharField(max_length=1000)
    album_genre = models.CharField(max_length=250)

    def __str__(self):
        return self.album_name + '-'+ self.album_artist

class Songs(models.Model):
    #Assuming an album has various artists and songs are of various genre
    song_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    song_artist = models.CharField(max_length=250)
    song_genre = models.CharField(max_length=250)
    song_length = models.TimeField()
    song_type = models.CharField(max_length=10)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title + '-' + self.song_artist
