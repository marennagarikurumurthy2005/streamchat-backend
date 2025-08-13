from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # direct playable URL (MP4, HLS, etc.) or YouTube fallback via youtube_id
    video_url = models.URLField(blank=True)
    youtube_id = models.CharField(max_length=64, blank=True)
    official_link = models.URLField(blank=True)

    def __str__(self):
        return self.title
