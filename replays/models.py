from django.db import models

from django.db.models.signals import pre_save, post_save, post_delete
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.conf import settings

from django.core.cache import cache

import os
import json
import datetime
import subprocess
from pathlib import Path


def to_base(num, b):
    numerals = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return ((num == 0) and numerals[0]) or (
        to_base(num // b, b).lstrip(numerals[0]) + numerals[num % b]
    )


# convert player name to base 62 integer, return string
def replay_hash_code(player):
    player_int = 0
    for char in player:
        player_int += ord(char)
    hash_code = to_base(player_int % 3844, 62)
    if len(hash_code) == 1:
        return "0" + hash_code
    return hash_code


# returns 2nd character for the replay code to indicate IN FinalA/B and UFO summon runs
def route_code(route):
    match route:
        case "FinalA":
            return "A"
        case "FinalB":
            return "B"
        case "UFOs":
            return "U"


def replay_dir(instance, filename):
    if instance.category is None:
        return f"replays/tmp.rpy"
    if instance.category.type == "LNN":
        replay_hash = replay_hash_code(instance.player)
        if instance.category.route:
            s = bytearray(replay_hash, "ascii")
            s[-1] = ord(route_code(instance.category.route))
            replay_hash = s.decode("ascii")
            # replay_hash[-1] = route_code(instance.category.route)
        return f"replays/lnn/{instance.player}/{instance.category.shot.game.code}{replay_hash}{instance.category.code}.rpy"
    path = f"replays/{instance.score}/{instance.category.shot.game.code}{instance.category.code}.rpy"
    return path


def game_name(num):
    match num:
        case 'th06': return 'EoSD'
        case 'th07': return 'PCB'
        case 'th08': return 'IN'
        case 'th09': return 'PoFV'
        case 'th095': return 'StB'
        case 'th10': return 'MoF'
        case 'th11': return 'SA'
        case 'th12': return 'UFO'
        case 'th125': return 'DS'
        case 'th128': return 'GFW'
        case 'th13': return 'TD'
        case 'th14': return 'DDC'
        case 'th15': return 'LoLK'
        case 'th16': return 'HSiFS'
        case 'th17': return 'WBaWC'
        case 'th18': return 'UM'
        case 'th20': return 'FW'


def difficulty_name(num):
    return ['Easy', 'Normal', 'Hard', 'Lunatic', 'Extra', 'Phantasm'][num]


def shot_name(game, data):
    shot_id = data['shot']
    if game == 'HSiFS':
        shot_id = data['season'] + shot_id * 4
    if game == 'WBaWC':
        shot_id = data['subshot'] + shot_id * 3
    if game == 'FW':
        shot_id = data['stones'][0] + shot_id * 8
    shot = ShotType.objects.get(game__short_name=game, order=shot_id)
    return shot.name


class Webhook(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField(max_length=128, unique=True)
    active = models.BooleanField(default=True)
    trigger_on_save = models.BooleanField(default=True)
    trigger_on_delete = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    full_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=16, unique=True)
    code = models.CharField(blank=True, max_length=16)
    number = models.FloatField(default=0)

    def __str__(self):
        return self.short_name


class ShotType(models.Model):
    class Meta:
        ordering = ["order"]

    name = models.CharField(max_length=128)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="shots")
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.game} {self.name}"


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    class CategoryType(models.TextChoices):
        lnn = "LNN"
        score = "Score"

    class Difficulty(models.TextChoices):
        easy = "Easy"
        normal = "Normal"
        hard = "Hard"
        lunatic = "Lunatic"
        extra = "Extra"
        phantasm = "Phantasm"

    class Region(models.TextChoices):
        western = "Western"
        eastern = "Eastern"

    type = models.CharField(choices=CategoryType, max_length=32)
    shot = models.ForeignKey(
        ShotType, on_delete=models.CASCADE, related_name="categories"
    )
    route = models.CharField(blank=True, max_length=16)
    difficulty = models.CharField(choices=Difficulty.choices, max_length=32)
    code = models.CharField(blank=True, max_length=16)
    region = models.CharField(
        max_length=16, choices=Region.choices, default=Region.eastern
    )

    def __str__(self):
        return f'{"(" + self.region + ") " if self.region == "Western" else ""}{self.shot} {self.route} {self.difficulty} {self.type}'


class Replay(models.Model):
    if os.path.exists("thrpy-parser/node_modules"):
        category = models.ForeignKey(
            Category, blank=True, null=True, on_delete=models.CASCADE, related_name="replays", help_text="If a replay file is included, the category will be set automatically. For LNNs, set this field manually."
        )
    else:
        category = models.ForeignKey(
            Category, on_delete=models.CASCADE, related_name="replays"
        )
    if os.path.exists("thrpy-parser/node_modules"):
        date = models.DateField(blank=True,null=True, help_text="If a replay file is included, the date will be set automatically.")
    else:
        date = models.DateField(blank=True,null=True)
    submitted_date = models.DateField(auto_now=True)
    player = models.CharField(max_length=128)
    replay = models.FileField(blank=True, upload_to=replay_dir)
    video = models.URLField(blank=True, max_length=256)
    if os.path.exists("thrpy-parser/node_modules"):
        score = models.BigIntegerField(default=0, help_text="If a replay file is included, the score will be set automatically.")
    else:
        score = models.BigIntegerField(default=0)
    verified = models.BooleanField(default=True)
    historical = models.BooleanField(default=False)

    def __str__(self):
        prefix = ""
        if self.historical == True:
            prefix = "(Historical) "
        elif self.verified == False:
            prefix = "(Unverified) "
        return f'{prefix}{self.category} by {self.player} from {self.submitted_date}'

    def clean(self):
        if self.pk:
            instance = Replay.objects.get(pk=self.pk)
            if self.date is None and instance.date is not None:
                raise ValidationError("Date cannot be removed")

            if self.category is None:
                raise ValidationError("Category cannot be removed")

            if self.replay != "" and instance.replay != "" and not Path(instance.replay.path).is_file():
                raise ValidationError("The currently saved replay was not found. Please clear the replay first")
        else:
            if self.replay == "" and self.date is None and self.category.region == Category.Region.eastern:
                raise ValidationError("This replay requires a date")

        if self.replay == "" and self.category is None:
            raise ValidationError("This replay requires a category")

    class Meta:
        indexes = [
            models.Index(
                fields=["category_id", "-score", "submitted_date"],
                name="replay_highscore_idx",
            ),
        ]


# if there are no higher scores, this score is WR, thus set Historical
@receiver(pre_save, sender=Replay)
def replay_save_handler(sender, instance, **kwargs):
    if instance.replay == "":
        if instance.video != "":
            instance.verified = True

        if instance.category.shot.game.short_name == "UDoALG":
            instance.score = 0

        if instance.category.region == Category.Region.eastern and instance.category.type == "Score" and instance.verified == True and instance.historical == False:
            higher_scores = Replay.objects.filter(category=instance.category, verified=True, score__gt=instance.score)
            higher_scores = higher_scores.count()
            if higher_scores == 0:
                instance.historical = True
    # temporary category to be able to save the replay
    elif instance.category is None:
        instance.category = Category.objects.get(code='dummy')


@receiver(post_save, sender=Replay)
def replay_save_handler(sender, instance, created, **kwargs):
    if instance.replay == "":
        return

    if os.path.exists("thrpy-parser/node_modules"):
        res = subprocess.run(["node", "get_data.js", instance.replay.path], capture_output=True, text=True)
        replay_data = json.loads(res.stdout)
        rewrite_rpy = False

        if instance.date is None:
            instance.date = replay_data["date"]
            Replay.objects.bulk_update([instance], ["date"])

        if instance.score == 0:
            instance.score = int(replay_data["score"])
            Replay.objects.bulk_update([instance], ["score"])
            rewrite_rpy = True

        # assume score run if temporary category
        if instance.category == Category.objects.get(code="dummy"):
            game = game_name(replay_data["game"])
            diff = difficulty_name(replay_data["difficulty"])
            shottype = shot_name(game, replay_data)
            shot = ShotType.objects.get(game__short_name=game, name=shottype)
            instance.category = Category.objects.get(type="Score", region=Category.Region.eastern, difficulty=diff, shot=shot)
            Replay.objects.bulk_update([instance], ["category"])
            rewrite_rpy = True

        if rewrite_rpy:
            old_path = Path(instance.replay.path)
            new_path = Path(replay_dir(instance, ""))
            os.renames(old_path, Path(settings.MEDIA_ROOT) / new_path)
            instance.replay.name = str(new_path)
            Replay.objects.bulk_update([instance], ["replay"])

    elif instance.category.shot.game.short_name == "UDoALG" and instance.score > 0:
        instance.score = 0
        Replay.objects.bulk_update([instance], ["score"])

    instance.verified = True
    Replay.objects.bulk_update([instance], ["verified"])

    if instance.category.region == Category.Region.eastern and instance.category.type == "Score" and instance.verified == True and instance.historical == False:
        higher_scores = Replay.objects.filter(category=instance.category, verified=True, score__gt=instance.score)
        higher_scores = higher_scores.count()
        if higher_scores == 0:
            instance.historical = True
            Replay.objects.bulk_update([instance], ["historical"])

    if created:
        return

    old_path = Path(instance.replay.path)
    new_path = Path(replay_dir(instance, ""))

    if new_path != old_path:
        os.renames(old_path, Path(settings.MEDIA_ROOT) / new_path)

        instance.replay.name = str(new_path)

        Replay.objects.bulk_update([instance], ["replay"])


@receiver(post_delete, sender=Replay)
def replay_delete_handler(sender, instance, **kwargs):
    if instance.replay == "":
        return
    path = Path(instance.replay.path)
    try:
        os.remove(path)
    except OSError:
        pass


def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("api_updated_at_timestamp", datetime.datetime.utcnow())


for model in [Category, Game, ShotType, Replay]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)
