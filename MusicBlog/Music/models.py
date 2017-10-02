from django.db import models

# Create your models here.
class Albums(models.Model):
    album_name = models.CharField(max_length= 50)
    album_artists = models.CharField(max_length =50)
    album_genre = models.CharField(max_length=250)
    def __str__(self):
        return self.album_name + '-'+ self.album_artist

class Songs(models.Model):
    song_album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    song_artist = models.CharField(max_length=250)
    song_genre = models.CharField(max_length=250)
    def __str__(self):
        return self.song_title + '-' + self.song_album + '-' + self.song_artist
