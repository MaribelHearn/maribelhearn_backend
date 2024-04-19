from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import ReplaySerializer
from ..models import Replay, Category


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("shot__game").filter(
        category__type=Category.CategoryType.score
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__shot__game", "category__shot"]
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination


class LNNiewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("shot__game").filter(
        category__type=Category.CategoryType.lnn
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__shot__game", "category__shot"]
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination
