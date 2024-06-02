from discord_webhook import DiscordWebhook, DiscordEmbed


def execute_webhook(webhook_url, title, data):
    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(title=title)
    for k, v in data.items():
        embed.add_embed_field(k, v)

    webhook.add_embed(embed)
    webhook.execute()
