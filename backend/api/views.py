from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Match, Post, Team, Tournament
from .serializers import (
    LogoutSerializer,
    MatchDetailSerializer,
    MatchSerializer,
    PostSerializer,
    RegisterSerializer,
    TeamSerializer,
    TournamentSerializer,
)


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data.get("username"))
            response.data["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        return response


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = TokenObtainPairSerializer.get_token(user)
    return Response(
        {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Logged out successfully."})


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health_view(request):
    return Response({"status": "ok"})


class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]


class TournamentListAPIView(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.AllowAny]


class MatchListAPIView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Match.objects.select_related("tournament", "team_one", "team_two", "winner").all()
        team_id = self.request.query_params.get("team")
        search = self.request.query_params.get("search")
        status_filter = self.request.query_params.get("status")

        if team_id:
            queryset = queryset.filter(Q(team_one_id=team_id) | Q(team_two_id=team_id))
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(tournament__name__icontains=search)
                | Q(team_one__name__icontains=search)
                | Q(team_two__name__icontains=search)
            )
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class MatchDetailAPIView(generics.RetrieveAPIView):
    serializer_class = MatchDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Match.objects.select_related(
            "tournament",
            "team_one",
            "team_two",
            "winner",
        ).prefetch_related(
            "team_one__players",
            "team_two__players",
            "maps__picked_by",
        )


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.select_related("author", "match").all()
        mine = self.request.query_params.get("mine")
        if mine == "true":
            if self.request.user.is_authenticated:
                return queryset.filter(author=self.request.user)
            return queryset.none()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.select_related("author", "match").filter(author=self.request.user)
