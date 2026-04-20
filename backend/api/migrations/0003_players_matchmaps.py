from django.db import migrations, models
import django.db.models.deletion


def seed_rosters_and_maps(apps, schema_editor):
    Team = apps.get_model("api", "Team")
    Player = apps.get_model("api", "Player")
    Match = apps.get_model("api", "Match")
    MatchMap = apps.get_model("api", "MatchMap")

    if Player.objects.exists() or MatchMap.objects.exists():
        return

    roster_data = {
        "Vitality": [
            ("ZywOo", "Mathieu Herbaut", "France", "AWPer", 1.31),
            ("apEX", "Dan Madesclaire", "France", "IGL", 1.02),
            ("Spinx", "Lotan Giladi", "Israel", "Rifler", 1.11),
            ("flameZ", "Shahar Shushan", "Israel", "Entry", 1.08),
            ("mezii", "William Merriman", "United Kingdom", "Support", 1.04),
        ],
        "Spirit": [
            ("donk", "Danil Kryshkovets", "Russia", "Star Rifler", 1.35),
            ("chopper", "Leonid Vishnyakov", "Russia", "IGL", 0.99),
            ("sh1ro", "Dmitriy Sokolov", "Russia", "AWPer", 1.18),
            ("zont1x", "Myroslav Plakhotia", "Ukraine", "Anchor", 1.05),
            ("magixx", "Boris Vorobiev", "Russia", "Support", 1.01),
        ],
        "Natus Vincere": [
            ("b1t", "Valerii Vakhovskyi", "Ukraine", "Rifler", 1.12),
            ("w0nderful", "Ihor Zhdanov", "Ukraine", "AWPer", 1.14),
            ("Aleksib", "Aleksi Virolainen", "Finland", "IGL", 0.98),
            ("jL", "Justinas Lekavicius", "Lithuania", "Entry", 1.07),
            ("iM", "Ivan Mihai", "Romania", "Lurker", 1.03),
        ],
        "FaZe": [
            ("frozen", "David Cernansky", "Slovakia", "Rifler", 1.15),
            ("broky", "Helvijs Saukants", "Latvia", "AWPer", 1.11),
            ("karrigan", "Finn Andersen", "Denmark", "IGL", 0.95),
            ("rain", "Havard Nygaard", "Norway", "Entry", 1.04),
            ("ropz", "Robin Kool", "Estonia", "Closer", 1.16),
        ],
    }

    teams = {team.name: team for team in Team.objects.all()}

    for team_name, players in roster_data.items():
        for nickname, full_name, country, role, rating in players:
            Player.objects.create(
                team=teams[team_name],
                nickname=nickname,
                full_name=full_name,
                country=country,
                role=role,
                rating=rating,
            )

    match_map_data = {
        "Vitality vs Spirit": [
            ("Inferno", 1, teams["Vitality"], "Vitality comfort pick"),
            ("Dust2", 2, teams["Spirit"], "Spirit want fast-paced duels"),
            ("Nuke", 3, None, "Likely decider"),
        ],
        "Natus Vincere vs FaZe": [
            ("Mirage", 1, teams["Natus Vincere"], "NAVI default-heavy opener"),
            ("Ancient", 2, teams["FaZe"], "FaZe punish weak mid control"),
            ("Inferno", 3, None, "Possible final map"),
        ],
        "Spirit vs Natus Vincere": [
            ("Anubis", 1, teams["Spirit"], "Spirit got space early"),
            ("Mirage", 2, teams["Natus Vincere"], "NAVI evened the series"),
            ("Dust2", 3, None, "Spirit closed on decider"),
        ],
    }

    matches = {match.title: match for match in Match.objects.all()}

    for match_title, maps in match_map_data.items():
        for name, order, picked_by, note in maps:
            MatchMap.objects.create(
                match=matches[match_title],
                name=name,
                order=order,
                picked_by=picked_by,
                note=note,
            )


def undo_rosters_and_maps(apps, schema_editor):
    apps.get_model("api", "MatchMap").objects.all().delete()
    apps.get_model("api", "Player").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_seed_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nickname", models.CharField(max_length=50)),
                ("full_name", models.CharField(blank=True, max_length=120)),
                ("country", models.CharField(max_length=80)),
                ("role", models.CharField(max_length=50)),
                ("rating", models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                (
                    "team",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="players", to="api.team"),
                ),
            ],
            options={"ordering": ["team__world_ranking", "nickname"]},
        ),
        migrations.CreateModel(
            name="MatchMap",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=40)),
                ("order", models.PositiveIntegerField()),
                ("note", models.CharField(blank=True, max_length=120)),
                (
                    "match",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="maps", to="api.match"),
                ),
                (
                    "picked_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="picked_maps",
                        to="api.team",
                    ),
                ),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.RunPython(seed_rosters_and_maps, undo_rosters_and_maps),
    ]
