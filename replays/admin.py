from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Category, Game, ShotType, Replay


# Register your models here.
@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = True
    search_fields = ["shot__game__short_name", "difficulty", "type", "shot__name"]
    exclude = ["id"]


@register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ["short_name"]
    exclude = ["id"]


@register(ShotType)
class ShotTypeAdmin(admin.ModelAdmin):
    list_select_related = True
    search_fields = ["game__short_name", "name"]
    exclude = ["id"]


@register(Replay)
class ReplayAdmin(admin.ModelAdmin):
    # list_select_related = ["category"]
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
    # raw_id_fields = ["category"]
    search_fields = ["player", "category__shot__game__short_name"]
    autocomplete_fields = ["category"]
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
        "video",
        "category",
    ]
    exclude = ["id"]
