from django.db import migrations


def seed_data(apps, schema_editor):
    Team = apps.get_model("api", "Team")
    Tournament = apps.get_model("api", "Tournament")
    Match = apps.get_model("api", "Match")

    if Team.objects.exists():
        return

    teams = {
        "Vitality": Team.objects.create(name="Vitality", country="France", world_ranking=1, logo_url="https://placehold.co/80x80/orange/111?text=VIT"),
        "Spirit": Team.objects.create(name="Spirit", country="Russia", world_ranking=2, logo_url="https://placehold.co/80x80/4d8bff/111?text=SPI"),
        "Natus Vincere": Team.objects.create(name="Natus Vincere", country="Ukraine", world_ranking=3, logo_url="https://placehold.co/80x80/f4d35e/111?text=NAVI"),
        "FaZe": Team.objects.create(name="FaZe", country="International", world_ranking=4, logo_url="https://placehold.co/80x80/ff5d73/111?text=FAZE"),
    }

    melbourne = Tournament.objects.create(
        name="JohnTV Masters Melbourne",
        location="Melbourne",
        tier="S-Tier",
        start_date="2026-05-02",
        end_date="2026-05-08",
    )
    spring = Tournament.objects.create(
        name="Spring Clash Europe",
        location="Berlin",
        tier="A-Tier",
        start_date="2026-05-10",
        end_date="2026-05-16",
    )

    Match.objects.create(
        title="Vitality vs Spirit",
        tournament=melbourne,
        team_one=teams["Vitality"],
        team_two=teams["Spirit"],
        match_time="2026-05-02T09:00:00Z",
        best_of=3,
        status="upcoming",
    )
    Match.objects.create(
        title="Natus Vincere vs FaZe",
        tournament=melbourne,
        team_one=teams["Natus Vincere"],
        team_two=teams["FaZe"],
        match_time="2026-05-02T12:30:00Z",
        best_of=3,
        status="live",
    )
    Match.objects.create(
        title="Spirit vs Natus Vincere",
        tournament=spring,
        team_one=teams["Spirit"],
        team_two=teams["Natus Vincere"],
        winner=teams["Spirit"],
        match_time="2026-04-16T16:00:00Z",
        best_of=3,
        status="finished",
    )


def undo_seed(apps, schema_editor):
    apps.get_model("api", "Post").objects.all().delete()
    apps.get_model("api", "Match").objects.all().delete()
    apps.get_model("api", "Tournament").objects.all().delete()
    apps.get_model("api", "Team").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, undo_seed),
    ]
