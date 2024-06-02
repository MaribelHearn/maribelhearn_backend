from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register

from .models import Category, Game, ShotType, Replay, Webhook


@register(Webhook)
class WebhookAdmin(ModelAdmin):
    list_display = ["name", "url", "active", "trigger_on_save", "trigger_on_delete"]


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["shot__game__short_name", "difficulty", "type", "shot__name"]
    list_display = ["id", "type", "difficulty", "shot", "route", "region", "code"]
    list_filter = ["type", "difficulty", "shot__game", "region"]
    exclude = ["id"]


@register(Game)
class GameAdmin(ModelAdmin):
    search_fields = ["short_name"]
    list_display = ["id", "short_name", "full_name", "number"]
    exclude = ["id"]


@register(ShotType)
class ShotTypeAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["game__short_name", "name"]
    list_display = ["id", "name", "game", "order"]
    list_editable = ["order", "name"]
    list_filter = ["game"]
    exclude = ["id"]


@register(Replay)
class ReplayAdmin(ModelAdmin):
    # list_select_related = ["category"]
    list_display = [
        "id",
        "category",
        "player",
        "score",
        "date",
        "video",
        "verified",
    ]
    # raw_id_fields = ["category"]
    search_fields = [
        "player",
        "category__shot__game__short_name",
        "category__shot__name",
        "category__difficulty",
    ]
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
