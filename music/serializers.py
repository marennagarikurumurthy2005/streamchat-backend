from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    spotify_embed_url = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'artist', 'audio_url', 'spotify_id', 'spotify_embed_url', 'official_link']
        model = Song

    def get_spotify_embed_url(self, obj):
        # works for track IDs
        if obj.spotify_id:
            return f"https://open.spotify.com/embed/track/{obj.spotify_id}"
        return None
