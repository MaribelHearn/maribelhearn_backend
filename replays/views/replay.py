from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter

from ..serializers import ReplaySerializer
from ..models import Replay, Category


class ReplayFilter(FilterSet):
    game = CharFilter(
        field_name="category__shot__game__short_name", lookup_expr="exact"
    )
    shot = CharFilter(field_name="category__shot__name", lookup_expr="exact")
    player = CharFilter(field_name="player", lookup_expr="exact")


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("category__shot__game").filter(
        category__type=Category.CategoryType.score
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReplayFilter
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination


class LNNiewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("category__shot__game").filter(
        category__type=Category.CategoryType.lnn
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReplayFilter
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination
