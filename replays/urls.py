from rest_framework import routers

from .views import category, replay

router = routers.DefaultRouter()
router.register("score", replay.ScoreViewSet, "score")
router.register("lnn", replay.LNNiewSet, "lnn")
router.register("category", category.CategoryViewSet, "category")

urlpatterns = router.urls
