from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.decorators import register

from .models import Category, Game, ShotType, Replay, Webhook

from difflib import SequenceMatcher
from functools import reduce


@register(Webhook)
class WebhookAdmin(ModelAdmin):
    list_display = ["name", "url", "active", "trigger_on_save", "trigger_on_delete"]


class ReplayInline(TabularInline):
    model = Replay
    extra = 0
    classes = ["collapse"]


class ShotInline(TabularInline):
    model = ShotType
    extra = 0
    classes = ["collapse"]


class CategoryInline(TabularInline):
    model = Category
    extra = 0
    classes = ["collapse"]


def activation(x):
    return x ** 2


def calculate_rank(category, query):
    shot_name_matcher = SequenceMatcher(a=category.shot.name, b=query)
    game_matcher = SequenceMatcher(a=category.shot.game.short_name, b=query)
    difficulty_matcher = SequenceMatcher(a=category.difficulty, b=query)
    route_matcher = SequenceMatcher(a=category.route, b=query)
    type_matcher = SequenceMatcher(a=category.type, b=query)

    shot_name_ratio = shot_name_matcher.ratio()
    game_ratio = game_matcher.ratio()
    difficulty_ratio = difficulty_matcher.ratio()
    route_ratio = route_matcher.ratio()
    type_ratio = type_matcher.ratio()

    activated = reduce(lambda x, y: x + activation(y), [shot_name_ratio, game_ratio, difficulty_ratio, route_ratio, type_ratio], 0)

    # You can adjust the weighting of shot_name_ratio and code_ratio as needed
    # For example, if shot_name is more important, give it a higher weight
    return activated


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["shot__game__short_name", "difficulty", "type", "shot__name"]
    list_display = ["id", "type", "difficulty", "shot", "route", "region", "code"]
    list_filter = ["type", "difficulty", "shot__game", "region"]
    exclude = ["id"]
    inlines = [ReplayInline]

    def get_search_results(self, request, queryset, search_term):
        queryset = sorted(queryset, key=lambda x: calculate_rank(x, search_term), reverse=True)
        return queryset, False


@register(Game)
class GameAdmin(ModelAdmin):
    search_fields = ["short_name"]
    list_display = ["id", "short_name", "full_name", "number"]
    exclude = ["id"]
    inlines = [ShotInline]


@register(ShotType)
class ShotTypeAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["game__short_name", "name"]
    list_display = ["id", "name", "game", "order"]
    list_editable = ["order", "name"]
    list_filter = ["game"]
    exclude = ["id"]
    inlines = [CategoryInline]


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
        "historical",
    ]
    # raw_id_fields = ["category"]
    search_fields = [
        "player",
        "category__shot__name__contains",
        "category__difficulty__exact",
    ]
    autocomplete_fields = ["category"]
    list_filter = [
        ("verified", admin.BooleanFieldListFilter),
        ("historical", admin.BooleanFieldListFilter),
        ("category__type", admin.ChoicesFieldListFilter),
        ("category__difficulty", admin.ChoicesFieldListFilter),
        ("category__region", admin.ChoicesFieldListFilter),
        ("category__shot__game", admin.RelatedFieldListFilter),
    ]
    list_editable = [
        "score",
        "verified",
        "historical",
        "player",
        "date",
        "video",
        "category",
    ]
