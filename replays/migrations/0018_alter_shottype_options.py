# Generated by Django 5.0.4 on 2024-05-31 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("replays", "0017_alter_game_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shottype",
            options={"ordering": ["order"]},
        ),
    ]