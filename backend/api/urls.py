from django.urls import path

from .views import (
    LoginView,
    MatchDetailAPIView,
    MatchListAPIView,
    PostDetailAPIView,
    PostListCreateAPIView,
    TeamListAPIView,
    TournamentListAPIView,
    health_view,
    logout_view,
    register_view,
)


urlpatterns = [
    path("health/", health_view),
    path("auth/register/", register_view),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", logout_view),
    path("teams/", TeamListAPIView.as_view()),
    path("tournaments/", TournamentListAPIView.as_view()),
    path("matches/", MatchListAPIView.as_view()),
    path("matches/<int:pk>/", MatchDetailAPIView.as_view()),
    path("posts/", PostListCreateAPIView.as_view()),
    path("posts/<int:pk>/", PostDetailAPIView.as_view()),
]
