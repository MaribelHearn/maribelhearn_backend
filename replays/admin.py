from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.decorators import register
from django.contrib.admin.widgets import AutocompleteSelect
from django.db.models import Case, When, IntegerField
from import_export.admin import ImportExportModelAdmin

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
    # western records are unused except for the dummy category
    if category.region == Category.Region.western:
        return 0
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


class FastAutocompleteSelect(AutocompleteSelect):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-ajax--delay"] = 50
        return attrs


LNN_MAINTAINERS_GROUP = "LNN Maintainers"
WR_MAINTAINERS_GROUP = "WR Maintainers"


def restrict_queryset_to_maintained_category_type(request, queryset, category_type_lookup):
    """
    Scopes a queryset to the category type a maintainer is responsible for.

    LNN maintainers only see LNN categories/replays, WR maintainers only see
    Score ones. Anyone in both groups, neither group, or a superuser sees
    everything (unchanged behavior for existing staff).
    """
    if request.user.is_superuser:
        return queryset

    groups = set(request.user.groups.values_list("name", flat=True))
    is_lnn_maintainer = LNN_MAINTAINERS_GROUP in groups
    is_wr_maintainer = WR_MAINTAINERS_GROUP in groups

    if is_lnn_maintainer and not is_wr_maintainer:
        return queryset.filter(**{category_type_lookup: Category.CategoryType.lnn})
    if is_wr_maintainer and not is_lnn_maintainer:
        return queryset.filter(**{category_type_lookup: Category.CategoryType.score})
    return queryset


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["shot__game__short_name", "difficulty", "type", "shot__name"]
    list_display = ["id", "type", "difficulty", "shot", "route", "region", "code"]
    list_filter = ["type", "difficulty", "shot__game", "region"]
    exclude = ["id"]
    inlines = [ReplayInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return restrict_queryset_to_maintained_category_type(request, queryset, "type")

    def get_search_results(self, request, queryset, search_term):
        queryset = queryset.select_related("shot", "shot__game")
        if not search_term:
            return queryset, False

        ranked_pks = [
            obj.pk
            for obj in sorted(
                queryset, key=lambda x: calculate_rank(x, search_term), reverse=True
            )
        ]
        if not ranked_pks:
            return queryset.none(), False

        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(ranked_pks)],
            output_field=IntegerField(),
        )
        queryset = queryset.filter(pk__in=ranked_pks).order_by(preserved_order)
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
class ReplayAdmin(ImportExportModelAdmin):
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return restrict_queryset_to_maintained_category_type(
            request, queryset, "category__type"
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["widget"] = FastAutocompleteSelect(db_field, self.admin_site)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
