# Generated by Django 5.0.4 on 2024-05-31 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("replays", "0016_shottype_order_alter_replay_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="number",
            field=models.FloatField(default=0),
        ),
    ]