from .models import Replay, Webhook, Category, replay_dir

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from urllib.parse import quote

from .tasks import execute_webhook

from django_q.tasks import async_task


@receiver(post_save, sender=Replay, dispatch_uid="webhooks_signal_save")
def send_discord_webhook_save(sender, instance: Replay, created, **kwargs):
    webhooks = Webhook.objects.filter(active=True, trigger_on_save=True)

    if created:
        title = "Replay created"
    else:
        title = "Replay updated"

    for webhook in webhooks:
        data = {}
        data["Category"] = str(instance.category)
        data["Player"] = instance.player
        if instance.category.type == Category.CategoryType.score:
            data["Score"] = instance.score

        if instance.video != "":
            data["Video"] = instance.video
        data["Date"] = str(instance.date)

        if instance.replay is not None:
            name = replay_dir(instance, "")
            url = settings.MEDIA_URL + quote(name)
            data["Replay"] = url

        async_task(execute_webhook, webhook.url, title, data)


@receiver(post_delete, sender=Replay, dispatch_uid="webhooks_signal_delete")
def send_discord_webhook_delete(sender, instance: Replay, **kwargs):
    webhooks = Webhook.objects.filter(active=True, trigger_on_delete=True)

    for webhook in webhooks:
        data = {}
        data["Category"] = str(instance.category)
        data["Player"] = instance.player

        if instance.category.type == Category.CategoryType.score:
            data["Score"] = instance.score

        data["Date"] = str(instance.date)

        async_task(execute_webhook, webhook.url, "Replay deleted", data)
