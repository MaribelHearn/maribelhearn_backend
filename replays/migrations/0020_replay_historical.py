# Generated by Django 5.0.4 on 2024-08-23 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("replays", "0019_webhook"),
    ]

    operations = [
        migrations.AddField(
            model_name="replay",
            name="historical",
            field=models.BooleanField(default=False),
        ),
    ]
