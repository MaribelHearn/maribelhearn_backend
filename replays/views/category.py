from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet,
    CharFilter,
    MultipleChoiceFilter,
    OrderingFilter,
    ChoiceFilter,
)

from ..serializers import CategorySerializer
from ..models import Category


class CategoryFilter(FilterSet):
    game = CharFilter(field_name="shot__game__short_name", lookup_expr="exact")
    shot = CharFilter(field_name="shot__name", lookup_expr="exact")
    difficulty = MultipleChoiceFilter(
        field_name="difficulty",
        choices=Category.Difficulty.choices,
        lookup_expr="exact",
    )
    type = MultipleChoiceFilter(
        field_name="type", choices=Category.CategoryType.choices
    )
    route = CharFilter(field_name="route")
    region = ChoiceFilter(
        field_name="region", choices=Category.Region.choices
    )

    ordering = OrderingFilter(
        fields=(
            ("shot__game__short_name", "game"),
            ("shot__name", "shot"),
            ("region", "region"),
        ),
    )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("shot__game")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    serializer_class = CategorySerializer
