from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from rest_framework_extensions.cache.mixins import CacheResponseMixin

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    MultipleChoiceFilter,
    OrderingFilter,
)

from django.db.models import Count
from django.db.models import Case, When
from django.db.models import F, Window
from django.db.models.functions import RowNumber

from ..serializers import ReplaySerializer, PlayersSerializer
from ..models import Replay, Category
from ..cache import ObjectKeyConstructor, ListKeyConstructor


class DifficultyOrderingFilter(OrderingFilter):
    """
    Custom ordering filter that adds difficulty-based sorting.
    Implements custom sorting logic for Category difficulty levels.
    
    Adds two new ordering options:
    - 'difficulty' - Order by difficulty level (Easy, Normal, Hard, etc.)
    - '-difficulty' - Reverse difficulty order
    """
    def __init__(self, *args, **kwargs):
        """Initialize filter with custom sorting choices for difficulty"""
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("difficulty", "Difficulty"),
            ("-difficulty", "Difficulty (descending)"),
        ]

    def get_ordering_value(self, param):
        """
        Convert ordering parameter to actual model field ordering
        
        Args:
            param (str): Ordering parameter from query string
            
        Returns:
            Case: Conditional expression for database ordering
        """
        old_param = param
        descending = param.startswith("-")
        param = param[1:] if descending else param
        multiplier = -1 if descending else 1

        diff_values = Category.Difficulty.values

        if param == "difficulty":
            preferred = Case(
                *(
                    When(category__difficulty=id, then=pos * multiplier)
                    for pos, id in enumerate(diff_values, start=1)
                )
            )
            return preferred
        else:
            return super().get_ordering_value(old_param)


class ReplayFilter(FilterSet):
    """
    FilterSet for Replay model with advanced filtering options

    Filters:
    - game: Filter by game short name
    - shot: Filter by shot type name
    - difficulty: Multi-select difficulty level filter
    - type: Category type filter
    - region: Region filter
    - verified: Boolean verified status filter
    - Custom date range filters
    - Complex ordering support
    """
    score__wr = BooleanFilter(
        field_name="score", method="filter_is_wr", label="Score is WR"
    )

    game__gte = CharFilter(
        field_name="category__shot__game__number", lookup_expr="gte"
    )
    game__lte = CharFilter(
        field_name="category__shot__game__number", lookup_expr="lte"
    )
    game__contains = CharFilter(
        field_name="category__shot__game__short_name", lookup_expr="contains"
    )
    shot__contains = CharFilter(
        field_name="category__shot__name", lookup_expr="contains"
    )

    game = CharFilter(field_name="category__shot__game__short_name")
    shot = CharFilter(field_name="category__shot__name")
    route = CharFilter(field_name="category__route")

    difficulty = MultipleChoiceFilter(
        field_name="category__difficulty",
        choices=Category.Difficulty.choices,
        lookup_expr="exact",
    )
    type = ChoiceFilter(
        field_name="category__type", choices=Category.CategoryType.choices
    )
    region = ChoiceFilter(
        field_name="category__region", choices=Category.Region.choices
    )
    verified = BooleanFilter(field_name="verified", lookup_expr="exact")
    historical = BooleanFilter(field_name="historical", lookup_expr="exact")
    ordering = DifficultyOrderingFilter(
        fields=(
            ("category__shot__game__number", "game"),
            ("category__shot__order", "shot"),
            ("category__route", "route"),
            ("category__region", "region"),
            ("date", "date"),
            ("score", "score"),
            ("player", "player"),
            ("verified", "verified"),
            ("historical", "historical"),
        ),
    )

    class Meta:
        model = Replay
        fields = {
            "date": ["gt", "lt", "exact", "isnull"],
            "player": ["exact", "contains"],
            "score": ["gte", "lte", "wr"],
        }

    def filter_is_wr(self, qs, name, value):
        ranked = Replay.objects.filter(
            category__type="Score",
            verified=True,
        ).annotate(
            rn=Window(
                expression=RowNumber(),
                partition_by=[F("category_id")],
                order_by=[F("score").desc(), F("submitted_date").asc()],
            )
        )

        highscores = Replay.objects.filter(
            pk__in=ranked.filter(rn=1).values("pk")
        ).select_related("category", "category__shot")

        return highscores


class ReplayViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing replays
    
    Provides full CRUD operations for Replay records with:
    - Prefetched related game data
    - Authentication protection for write operations
    - Advanced filtering and ordering
    - Caching support
    - Pagination
    
    Additional actions:
    - players: Get unique player lists for different category types
    """
    queryset = Replay.objects.prefetch_related("category__shot__game")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReplaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReplayFilter
    pagination_class = pagination.LimitOffsetPagination
    object_cache_key_fun = ObjectKeyConstructor()
    list_cache_key_func = ListKeyConstructor()

    @action(
        methods=["GET"],
        detail=False,
        pagination_class=None,
        serializer_class=PlayersSerializer,
        renderer_classes=[JSONRenderer],
    )
    def players(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        score = (
            queryset.values_list("player", flat=True)
            .annotate(c=Count("player"))
            .filter(category__type="Score")
        )
        score = self.filter_queryset(score)
        lnn = (
            queryset.values_list("player", flat=True)
            .annotate(c=Count("player"))
            .filter(category__type="LNN")
        )
        lnn = self.filter_queryset(lnn)
        result = {"score": list(score), "lnn": list(lnn)}
        serializer = self.get_serializer(result)

        return Response(serializer.data)
