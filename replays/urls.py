from rest_framework import routers

from .views import category, replay, game

router = routers.DefaultRouter()
router.register("replay", replay.ReplayViewSet, basename="replay")
router.register("category", category.CategoryViewSet, basename="category")
router.register("game", game.GameViewSet, basename="game")

urlpatterns = router.urls
