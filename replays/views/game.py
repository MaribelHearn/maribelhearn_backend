from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet,
    CharFilter,
)


from rest_framework_extensions.cache.mixins import CacheResponseMixin

from ..serializers import GameSerializer
from ..models import Game
from ..cache import ObjectKeyConstructor, ListKeyConstructor


class GameFilter(FilterSet):
    """
    FilterSet for Game model
    
    Filters:
    - short_name: Filter by short name
    - number: Filter by number
    - release_date: Filter by release date
    """
    short_name = CharFilter(field_name="short_name", lookup_expr="exact")

    class Meta:
        model = Game
        fields = {
            "release_date": ["gt", "lt", "gte", "lte", "exact", "isnull"],
            "number": ["gt", "lt", "gte", "lte"],
        }


class GameViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing games
    
    Provides full CRUD operations for Game records with:
    - Default ordering by game number
    - Filtering by game short name
    - Authentication protection for write operations
    - Caching support
    """
    queryset = Game.objects.all().order_by("number")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameFilter
    serializer_class = GameSerializer
    object_cache_key_fun = ObjectKeyConstructor()
    list_cache_key_func = ListKeyConstructor()
