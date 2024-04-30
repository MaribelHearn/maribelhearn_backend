from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter, OrderingFilter

from ..serializers import ReplaySerializer
from ..models import Replay, Category


class ReplayFilter(FilterSet):
    game = CharFilter(
        field_name="category__shot__game__short_name", lookup_expr="exact"
    )
    shot = CharFilter(field_name="category__shot__name", lookup_expr="exact")
    player = CharFilter(field_name="player", lookup_expr="exact")
    ordering = OrderingFilter(
        fields=(
            ("category__shot__game__short_name", "game"),
            ("category__shot__name", "shot"),
            ("date", "date"),
        ),
    )


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("category__shot__game").filter(
        category__type=Category.CategoryType.score
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReplayFilter
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination


class LNNiewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("category__shot__game").filter(
        category__type=Category.CategoryType.lnn
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReplayFilter
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination
