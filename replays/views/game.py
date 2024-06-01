from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework_extensions.cache.mixins import CacheResponseMixin

from ..serializers import GameSerializer
from ..models import Game
from ..cache import ObjectKeyConstructor, ListKeyConstructor


class GameViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Game.objects.prefetch_related("shots__categories__replays").order_by(
        "number"
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["short_name"]
    serializer_class = GameSerializer
    object_cache_key_fun = ObjectKeyConstructor()
    list_cache_key_func = ListKeyConstructor()
