# Generated by Django 5.0.4 on 2024-05-01 20:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("replays", "0006_category_route"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="shot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shots",
                to="replays.shottype",
            ),
        ),
        migrations.AlterField(
            model_name="replay",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replays",
                to="replays.category",
            ),
        ),
    ]