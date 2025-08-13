from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    youtube_embed_url = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'description', 'video_url', 'youtube_id', 'youtube_embed_url', 'official_link']
        model = Movie

    def get_youtube_embed_url(self, obj):
        if obj.youtube_id:
            return f"https://www.youtube.com/embed/{obj.youtube_id}"
        return None
