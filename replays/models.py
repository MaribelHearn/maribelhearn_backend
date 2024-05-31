from django.db import models

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from django.core.cache import cache

import os
import datetime
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
    if instance.category.type == "LNN":
        replay_hash = replay_hash_code(instance.player)
        if instance.category.route:
            s = bytearray(replay_hash, "ascii")
            s[-1] = ord(route_code(instance.category.route))
            replay_hash = s.decode("ascii")
            # replay_hash[-1] = route_code(instance.category.route)
        return f"replays/lnn/{instance.player}/{instance.category.shot.game.code}{replay_hash}{instance.category.code}.rpy"
    return f"replays/{instance.category.shot.game.code}{instance.category.code}.rpy"


class Game(models.Model):
    full_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=16, unique=True)
    code = models.CharField(blank=True, max_length=16)
    number = models.FloatField(default=0)

    def __str__(self):
        return self.short_name


class ShotType(models.Model):
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
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="replays"
    )
    date = models.DateField(blank=True, null=True)
    submitted_date = models.DateField(auto_now=True)
    player = models.CharField(max_length=128)
    replay = models.FileField(blank=True, upload_to=replay_dir)
    video = models.URLField(blank=True, max_length=256)
    score = models.BigIntegerField(default=0)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return f'{"(Unverified) " if self.verified == False else ""}{self.category} by {self.player} from {self.submitted_date}'


@receiver(post_save, sender=Replay)
def replay_save_handler(sender, instance, created, **kwargs):
    if created:
        return
    if instance.replay == "":
        return
    old_path = Path(instance.replay.path)
    new_path = Path(replay_dir(instance, ""))
    os.renames(old_path, Path(settings.MEDIA_ROOT) / new_path)

    instance.replay.name = str(new_path)

    post_save.disconnect(replay_save_handler, sender=Replay)
    instance.save()
    post_save.connect(replay_save_handler, sender=Replay)


def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("api_updated_at_timestamp", datetime.datetime.utcnow())


for model in [Category, Game, ShotType, Replay]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)
