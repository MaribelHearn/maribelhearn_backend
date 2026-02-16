from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.decorators import register
from django.contrib.admin.widgets import AutocompleteSelect
from django.core.cache import cache

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
    return x**2


def calculate_rank(category, query):
    shot_name_matcher = SequenceMatcher(a=category.shot.name.lower(), b=query.lower())
    game_matcher = SequenceMatcher(
        a=category.shot.game.short_name.lower(), b=query.lower()
    )
    difficulty_matcher = SequenceMatcher(a=category.difficulty.lower(), b=query.lower())
    route_matcher = SequenceMatcher(a=category.route.lower(), b=query.lower())
    type_matcher = SequenceMatcher(a=category.type.lower(), b=query.lower())

    shot_name_ratio = shot_name_matcher.ratio()
    game_ratio = game_matcher.ratio()
    difficulty_ratio = difficulty_matcher.ratio()
    route_ratio = route_matcher.ratio()
    type_ratio = type_matcher.ratio()

    activated = reduce(
        lambda x, y: x + activation(y),
        [shot_name_ratio, game_ratio, difficulty_ratio, route_ratio, type_ratio],
        0,
    )

    # You can adjust the weighting of shot_name_ratio and code_ratio as needed
    # For example, if shot_name is more important, give it a higher weight
    return activated


def get_cached_categories():
    key = "categories_cache"
    data = cache.get(key)

    if data is None:
        data = list(Category.objects.all().select_related("shot", "shot__game"))
        cache.set(key, data, 3600)

    return data


class FastAutocompleteSelect(AutocompleteSelect):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-ajax--delay"] = 50
        return attrs


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["shot__game__short_name", "difficulty", "type", "shot__name"]
    list_display = ["id", "type", "difficulty", "shot", "route", "region", "code"]
    list_filter = ["type", "difficulty", "shot__game", "region"]
    exclude = ["id"]
    inlines = [ReplayInline]

    def get_search_results(self, request, queryset, search_term):
        queryset = get_cached_categories()
        queryset = sorted(
            queryset, key=lambda x: calculate_rank(x, search_term), reverse=True
        )
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["widget"] = FastAutocompleteSelect(db_field, self.admin_site)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
