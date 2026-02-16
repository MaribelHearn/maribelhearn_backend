from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category


class ReplaysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "replays"

    def ready(self):
        from . import signals


@receiver([post_save, post_delete], sender=Category)
def clear_my_model_cache(sender, **kwargs):
    cache.delete("categories_cache")
