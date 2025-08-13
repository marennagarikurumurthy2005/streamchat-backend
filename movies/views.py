import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.models import SearchHistory

@api_view(["GET"])
def get_movies(request):
    query = request.GET.get("query", "")
    if not query:
         return Response({"error": "Query is required"}, status=400)

    url = "https://api.themoviedb.org/3/search/movie"
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
        results.append({
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None,
            "tmdb_url": f"https://www.themoviedb.org/movie/{movie.get('id')}" if movie.get('id') else None
        })

    # Save search history if user is authenticated
    if request.user.is_authenticated:
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            result_type="movie"
        )

    return Response(results)
