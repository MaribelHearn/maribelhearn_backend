from django.db import models


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
    print(instance)
    if instance.category.type == "LNN":
        replay_hash = replay_hash_code(instance.player)
        if instance.category.route:
            replay_hash[-1] = route_code(instance.category.route)
        return f"replays/lnn/{instance.player}/{instance.category.shot.game.code}{replay_hash}{instance.category.code}.rpy"
    return f"replays/{instance.category.shot.game.code}{instance.category.code}.rpy"


class Game(models.Model):
    full_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=16, unique=True)
    code = models.CharField(blank=True, max_length=16)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name


class ShotType(models.Model):
    name = models.CharField(max_length=128)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="shots")

    def __str__(self):
        return f"{self.game} {self.name}"


class Category(models.Model):
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
    date = models.DateField(blank=True)
    submitted_date = models.DateField(auto_now=True)
    player = models.CharField(max_length=128)
    replay = models.FileField(blank=True, upload_to=replay_dir)
    video = models.URLField(blank=True, max_length=256)
    score = models.BigIntegerField(default=0)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category} by {self.player} from {self.submitted_date}"
