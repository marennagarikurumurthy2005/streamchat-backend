import json, asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from movies.services import search_movie_by_query, get_movie_trailers, get_watch_providers
from music.services import search_song

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('message','')
        username = data.get('username','guest')
        response = {'type':'text','text':f'You said: {text}'}

        if text.lower().startswith('movie '):
            q = text[6:].strip()
            movie = await asyncio.get_event_loop().run_in_executor(None, search_movie_by_query, q)
            if movie:
                trailers = await asyncio.get_event_loop().run_in_executor(None, get_movie_trailers, movie['id'])
                providers = await asyncio.get_event_loop().run_in_executor(None, get_watch_providers, movie['id'])
                response = {'type':'movie','title':movie['title'],'overview':movie['overview'],'poster':movie.get('poster'),'trailers':trailers,'providers':providers}
        elif text.lower().startswith('song '):
            q = text[5:].strip()
            song = await asyncio.get_event_loop().run_in_executor(None, search_song, q)
            if song:
                response = {'type':'song','title':song['title'],'artist':song['artist'],'spotify_url':song.get('spotify_url'),'preview_url':song.get('preview_url'),'album_cover':song.get('album_cover')}

        # save message optionally (no sender linkage here for simplicity)
        try:
            Message.objects.create(sender=User.objects.first(), content=json.dumps(response), metadata=response)
        except Exception:
            pass

        await self.send(text_data=json.dumps(response))
