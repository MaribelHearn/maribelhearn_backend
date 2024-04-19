from django.db import models


class Game(models.Model):
    full_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.short_name


class ShotType(models.Model):
    name = models.CharField(max_length=128)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

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

    type = models.CharField(choices=CategoryType, max_length=32)
    shot = models.ForeignKey(ShotType, on_delete=models.CASCADE)
    difficulty = models.CharField(choices=Difficulty.choices, max_length=32)

    def __str__(self):
        return f"{self.shot} {self.difficulty} {self.type}"


class Replay(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    submitted_date = models.DateField(auto_now=True)
    player = models.CharField(max_length=128)
    replay = models.URLField(blank=True, max_length=256)
    video = models.URLField(blank=True, max_length=256)

    def __str__(self):
        return f"{self.category} by {self.player} from {self.submitted_date}"
