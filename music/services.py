import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
_sp = None
def _get_sp():
    global _sp
    if _sp is None:
        auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        _sp = spotipy.Spotify(auth_manager=auth)
    return _sp

def search_song(query):
    if not CLIENT_ID or not CLIENT_SECRET or not query: return None
    sp = _get_sp()
    r = sp.search(q=query, type='track', limit=1)
    items = r.get('tracks', {}).get('items', [])
    if items:
        t = items[0]
        return {'title': t['name'], 'artist': t['artists'][0]['name'], 'spotify_url': t['external_urls']['spotify'], 'preview_url': t.get('preview_url'), 'album_cover': t['album']['images'][0]['url'] if t['album']['images'] else None}
    return None
