from django.db import models
from django.conf import settings

class SearchHistory(models.Model):
    MOVIE = 'movie'
    SONG = 'song'
    BOTH = 'both'
    TYPE_CHOICES = [(MOVIE, 'Movie'), (SONG, 'Song'), (BOTH, 'Both')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='searches')
    query = models.CharField(max_length=255)
    search_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=BOTH)
    created_at = models.DateTimeField(auto_now_add=True)

    # optional linkage to last clicked resource (for future)
    result_type = models.CharField(max_length=10, blank=True)  # 'movie' or 'song'
    result_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.query} ({self.search_type})"
    

    
class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    result_type = models.CharField(max_length=50)  # movie or song
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query