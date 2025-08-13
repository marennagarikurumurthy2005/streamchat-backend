import base64
import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chat.models import SearchHistory

SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET

def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    auth = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}
    res = requests.post(url, headers=headers, data=data)
    return res.json().get("access_token")

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # optional, only if you want auth
def get_songs(request):
    query = request.GET.get("query", "")
    if not query:
        return Response({"error": "Query is required"}, status=400)

    token = get_spotify_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 10}
    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    results = []
    for track in data.get("tracks", {}).get("items", []):
        results.append({
            "title": track.get("name"),
            "artist": ", ".join([artist["name"] for artist in track.get("artists", [])]),
            "spotify_url": track.get("external_urls", {}).get("spotify"),
            "embed_url": f"https://open.spotify.com/embed/track/{track.get('id')}"
        })

    # Save search history if user is authenticated
    if request.user.is_authenticated:
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            result_type="song"
        )

    return Response(results)
