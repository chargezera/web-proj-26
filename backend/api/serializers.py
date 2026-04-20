from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Match, MatchMap, Player, Post, Team, Tournament


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        token = RefreshToken(self.validated_data["refresh"])
        token.blacklist()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "country", "world_ranking", "logo_url"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "nickname", "full_name", "country", "role", "rating"]


class TeamRosterSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "country", "world_ranking", "logo_url", "players"]


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["id", "name", "location", "tier", "start_date", "end_date"]


class MatchSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    team_one = TeamSerializer(read_only=True)
    team_two = TeamSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "title",
            "tournament",
            "team_one",
            "team_two",
            "winner",
            "match_time",
            "best_of",
            "status",
        ]


class MatchMapSerializer(serializers.ModelSerializer):
    picked_by = TeamSerializer(read_only=True)

    class Meta:
        model = MatchMap
        fields = ["id", "name", "order", "picked_by", "note"]


class MatchDetailSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    team_one = TeamRosterSerializer(read_only=True)
    team_two = TeamRosterSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)
    maps = MatchMapSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "title",
            "tournament",
            "team_one",
            "team_two",
            "winner",
            "match_time",
            "best_of",
            "status",
            "maps",
        ]


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    match_title = serializers.CharField(source="match.title", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "match",
            "match_title",
            "title",
            "body",
            "confidence",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "author_username", "match_title", "created_at", "updated_at"]
