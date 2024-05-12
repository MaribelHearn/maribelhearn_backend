from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.renderers import JSONRenderer

from drf_spectacular.utils import extend_schema

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet,
    CharFilter,
    ChoiceFilter,
    MultipleChoiceFilter,
    OrderingFilter,
)

from django.db.models import Count

from ..serializers import ReplaySerializer, PlayersSerializer
from ..models import Replay, Category


class ReplayFilter(FilterSet):
    game = CharFilter(
        field_name="category__shot__game__short_name", lookup_expr="exact"
    )
    shot = CharFilter(field_name="category__shot__name", lookup_expr="exact")
    player = CharFilter(field_name="player", lookup_expr="exact")
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
    ordering = OrderingFilter(
        fields=(
            ("category__shot__game__number", "game"),
            ("category__shot__name", "shot"),
            ("category__region", "region"),
            ("date", "date"),
            ("score", "score"),
            ("verified", "verified"),
        ),
    )


class ReplayViewSet(viewsets.ModelViewSet):
    queryset = Replay.objects.prefetch_related("category__shot__game")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReplayFilter
    serializer_class = ReplaySerializer
    pagination_class = pagination.LimitOffsetPagination

    @extend_schema(responses={200: PlayersSerializer})
    @action(
        methods=["GET"],
        detail=False,
        pagination_class=None,
        filter_backends=[],
        serializer_class=PlayersSerializer,
        renderer_classes=[JSONRenderer],
    )
    def players(self, request):
        score = (
            Replay.objects.values_list("player", flat=True)
            .annotate(c=Count("player"))
            .filter(category__type="Score")
        )
        lnn = (
            Replay.objects.values_list("player", flat=True)
            .annotate(c=Count("player"))
            .filter(category__type="LNN")
        )
        result = {"score": list(score), "lnn": list(lnn)}
        return Response(result)
