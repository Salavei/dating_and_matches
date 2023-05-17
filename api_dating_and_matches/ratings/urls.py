from django.urls import path
from ratings.views import MatchesView


urlpatterns = [
    path('user/matches/', MatchesView.as_view(), name='matches'),
]