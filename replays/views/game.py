from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import GameSerializer
from ..models import Game


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.prefetch_related("shots__categories__replays")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["short_name"]
    serializer_class = GameSerializer
