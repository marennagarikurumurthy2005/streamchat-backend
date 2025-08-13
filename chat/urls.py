from django.urls import path
from .views import SearchView, HistoryListView, HistoryClearView
from .views.search import unified_search
urlpatterns = [
    path('search/', SearchView.as_view(), name='chat-search'),
    path('history/', HistoryListView.as_view(), name='chat-history'),
    path('history/clear/', HistoryClearView.as_view(), name='chat-history-clear'),
    path('search/', unified_search, name='unified_search'),
]
