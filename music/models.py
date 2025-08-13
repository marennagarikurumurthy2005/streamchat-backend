from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    # direct playable audio or Spotify fallback via spotify_id
    audio_url = models.URLField(blank=True)
    spotify_id = models.CharField(max_length=128, blank=True)
    official_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist}".strip(" -")
