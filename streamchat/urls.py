from django.contrib import admin
from django.urls import path

# Import your views
from accounts.views import register, login_view, forgot_password, reset_password
from movies.views import get_movies
from music.views import get_songs
from chat.views import get_history  # we’ll create this
  

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('auth/register/', register),
    path('auth/login/', login_view),
    path('auth/forgot-password/', forgot_password),
    path('auth/reset-password/<int:uid>/<str:token>/', reset_password),

    # Search
    path('movies/search/', get_movies),
    path('music/search/', get_songs),
     

    # History
    path('history/', get_history),
]
