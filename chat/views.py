from rest_framework import permissions, views, generics, status
from rest_framework.response import Response
from django.db.models import Q

from .models import SearchHistory
from .serializers import SearchHistorySerializer

from movies.models import Movie
from movies.serializers import MovieSerializer
from music.models import Song
from music.serializers import SongSerializer
from rest_framework.decorators import api_view

class SearchView(views.APIView):
    """
    POST { "q": "Interstellar", "type": "movie|song|both" }
    Saves query to history for the authenticated user.
    Returns matching movies/songs with embed URLs.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        q = (request.data.get('q') or '').strip()
        stype = (request.data.get('type') or 'both').lower()
        if not q:
            return Response({'error': 'q is required'}, status=400)
        if stype not in ('movie', 'song', 'both'):
            stype = 'both'

        # Save history row
        SearchHistory.objects.create(
            user=request.user,
            query=q,
            search_type=stype
        )

        movies = songs = []
        if stype in ('movie', 'both'):
            m_qs = Movie.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))[:25]
            movies = MovieSerializer(m_qs, many=True).data

        if stype in ('song', 'both'):
            s_qs = Song.objects.filter(Q(title__icontains=q) | Q(artist__icontains=q))[:25]
            songs = SongSerializer(s_qs, many=True).data

        return Response({'query': q, 'type': stype, 'movies': movies, 'songs': songs}, status=200)

class HistoryListView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)

class HistoryClearView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        SearchHistory.objects.filter(user=request.user).delete()
        return Response(status=204)


@api_view(["GET"])
def get_history(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:20]
    data = [{
        "query": h.query,
        "type": h.result_type,
        "time": h.timestamp
    } for h in history]

    return Response({"history": data})


from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    user = authenticate(request, email=email, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    # Generate JWT token
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "message": "Login successful"
    })
