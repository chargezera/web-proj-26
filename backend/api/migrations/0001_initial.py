from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("country", models.CharField(max_length=80)),
                ("world_ranking", models.PositiveIntegerField()),
                ("logo_url", models.URLField(blank=True)),
            ],
            options={"ordering": ["world_ranking", "name"]},
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("location", models.CharField(max_length=120)),
                ("tier", models.CharField(max_length=40)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
            options={"ordering": ["start_date", "name"]},
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=140)),
                ("match_time", models.DateTimeField()),
                ("best_of", models.PositiveIntegerField(default=3)),
                (
                    "status",
                    models.CharField(
                        choices=[("upcoming", "Upcoming"), ("live", "Live"), ("finished", "Finished")],
                        default="upcoming",
                        max_length=20,
                    ),
                ),
                (
                    "team_one",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="home_matches", to="api.team"),
                ),
                (
                    "team_two",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="away_matches", to="api.team"),
                ),
                (
                    "tournament",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="matches", to="api.tournament"),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="wins",
                        to="api.team",
                    ),
                ),
            ],
            options={"ordering": ["match_time"]},
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=140)),
                ("body", models.TextField()),
                ("confidence", models.PositiveIntegerField(default=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posts", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "match",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posts", to="api.match"),
                ),
            ],
            options={"ordering": ["-updated_at"]},
        ),
    ]
