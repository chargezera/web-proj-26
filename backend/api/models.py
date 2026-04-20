from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=80)
    world_ranking = models.PositiveIntegerField()
    logo_url = models.URLField(blank=True)

    class Meta:
        ordering = ["world_ranking", "name"]

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    nickname = models.CharField(max_length=50)
    full_name = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=80)
    role = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)

    class Meta:
        ordering = ["team__world_ranking", "nickname"]

    def __str__(self) -> str:
        return self.nickname


class Tournament(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    tier = models.CharField(max_length=40)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["start_date", "name"]

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("finished", "Finished"),
    ]

    title = models.CharField(max_length=140)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_matches")
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="wins",
        null=True,
        blank=True,
    )
    match_time = models.DateTimeField()
    best_of = models.PositiveIntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")

    class Meta:
        ordering = ["match_time"]

    def __str__(self) -> str:
        return self.title


class MatchMap(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="maps")
    name = models.CharField(max_length=40)
    order = models.PositiveIntegerField()
    picked_by = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="picked_maps",
        null=True,
        blank=True,
    )
    note = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.match.title} - {self.name}"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=140)
    body = models.TextField()
    confidence = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
