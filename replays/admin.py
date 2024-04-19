from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Category, Game, ShotType, Replay


# Register your models here.
@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ["id"]


@register(Game)
class GameAdmin(admin.ModelAdmin):
    exclude = ["id"]


@register(ShotType)
class ShotTypeAdmin(admin.ModelAdmin):
    exclude = ["id"]


@register(Replay)
class ReplayAdmin(admin.ModelAdmin):
    exclude = ["id"]
