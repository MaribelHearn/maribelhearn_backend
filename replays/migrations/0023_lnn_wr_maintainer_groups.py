from django.db import migrations


LNN_MAINTAINERS_GROUP = "LNN Maintainers"
WR_MAINTAINERS_GROUP = "WR Maintainers"


def create_maintainer_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=LNN_MAINTAINERS_GROUP)
    Group.objects.get_or_create(name=WR_MAINTAINERS_GROUP)


def delete_maintainer_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=[LNN_MAINTAINERS_GROUP, WR_MAINTAINERS_GROUP]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("replays", "0022_replay_replay_highscore_idx"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_maintainer_groups, delete_maintainer_groups),
    ]
