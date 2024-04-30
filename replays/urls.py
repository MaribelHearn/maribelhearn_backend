from rest_framework import routers

from .views import category, replay, game

router = routers.DefaultRouter()
router.register("replay", replay.ReplayViewSet, "replay")
router.register("category", category.CategoryViewSet, "category")
router.register("game", game.GameViewSet, "game")

urlpatterns = router.urls
