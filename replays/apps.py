from django.apps import AppConfig


class ReplaysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "replays"

    def ready(self):
        from . import signals
