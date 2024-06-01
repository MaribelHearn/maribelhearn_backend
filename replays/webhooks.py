from discord_webhook import AsyncDiscordWebhook, DiscordEmbed

from .models import Replay, Webhook, Category, replay_dir

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from urllib.parse import quote


@receiver(post_save, sender=Replay, dispatch_uid="webhooks_signal_save")
async def send_discord_webhook_save(sender, instance: Replay, created, **kwargs):
    webhooks = Webhook.objects.filter(active=True, trigger_on_save=True)
    print("emit!")

    if created:
        title = "Replay created"
    else:
        title = "Replay updated"

    async for webhook in webhooks:
        print("hook!")
        discord_wh = AsyncDiscordWebhook(url=webhook.url)
        embed = DiscordEmbed(title=title)
        embed.add_embed_field("Category", str(instance.category))
        embed.add_embed_field("Player", instance.player)

        if instance.category.type is Category.CategoryType.score:
            embed.add_embed_field("Score", instance.score)

        if instance.video != "":
            embed.add_embed_field("Video", instance.video)

        embed.add_embed_field("Date", str(instance.date))

        if instance.replay is not None:
            name = replay_dir(instance, "")
            url = settings.MEDIA_URL + quote(name)
            embed.add_embed_field("Replay", url)

        discord_wh.add_embed(embed)
        await discord_wh.execute()


@receiver(post_delete, sender=Replay, dispatch_uid="webhooks_signal_delete")
async def send_discord_webhook_delete(sender, instance: Replay, **kwargs):
    webhooks = Webhook.objects.filter(active=True, trigger_on_delete=True)

    for webhook in webhooks:
        discord_wh = AsyncDiscordWebhook(url=webhook.url)
        embed = DiscordEmbed(title="Replay deleted")
        embed.add_embed_field("Category", str(instance.category))
        embed.add_embed_field("Player", instance.player)

        if instance.category.type is Category.CategoryType.score:
            embed.add_embed_field("Score", instance.score)

        embed.add_embed_field("Date", str(instance.date))

        discord_wh.add_embed(embed)
        await discord_wh.execute()
