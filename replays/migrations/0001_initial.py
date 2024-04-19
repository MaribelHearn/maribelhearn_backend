# Generated by Django 5.0.4 on 2024-04-05 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("LNN", "Lnn"), ("Score", "Score")], max_length=32
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("Easy", "Easy"),
                            ("Normal", "Normal"),
                            ("Hard", "Hard"),
                            ("Lunatic", "Lunatic"),
                            ("Extra", "Extra"),
                            ("Phantasm", "Phantasm"),
                        ],
                        max_length=32,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=128)),
                ("short_name", models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name="Replay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("submitted_date", models.DateField()),
                ("player", models.CharField(max_length=128)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="replays.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ShotType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="replays.game"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="category",
            name="shot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="replays.shottype"
            ),
        ),
    ]
