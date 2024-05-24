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
    list_select_related = True
    list_display = [
        "id",
        "player",
        "replay",
        "video",
        "score",
        "submitted_date",
        "date",
        "verified",
        "category",
    ]
    autocomplete_fields = ["category"]
    search_fields = ["player", "category__shot__game__short_name"]
    list_filter = [
        ("verified", admin.BooleanFieldListFilter),
        ("category__type", admin.ChoicesFieldListFilter),
        ("category__difficulty", admin.ChoicesFieldListFilter),
        ("category__region", admin.ChoicesFieldListFilter),
    ]
    list_editable = [
        "score",
        "verified",
        "player",
        "date",
        "submitted_date",
        "video",
        "category",
    ]
    exclude = ["id"]
