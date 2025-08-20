import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.models import SearchHistory

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_first_trailer_url(movie_id):
    """Fetch first YouTube trailer URL from TMDb."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return None
    videos = res.json().get("results", [])
    for v in videos:
        if v.get("site", "").lower() == "youtube" and v.get("type", "").lower() == "trailer":
            return f"https://www.youtube.com/embed/{v.get('key')}"
    return None

@api_view(["GET"])
def get_movies(request):
    query = request.GET.get("query", "")
    if not query:
        return Response({"error": "Query is required"}, status=400)

    # Search movies
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1,
        "include_adult": False
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return Response({"error": "TMDb API error"}, status=500)

    data = res.json()
    results = []

    for movie in data.get("results", []):
        movie_id = movie.get("id")
        tmdb_embed = get_first_trailer_url(movie_id) if movie_id else None

        # For full movie streaming, we use the TMDb ID as stream identifier
        stream = str(movie_id) if movie_id else None

        results.append({
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None,
            "tmdb_url": f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else None,
            "tmdb_embed": tmdb_embed,
            "stream": stream
        })

    # Save search history
    if request.user.is_authenticated:
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            result_type="movie"
        )

    return Response(results)
