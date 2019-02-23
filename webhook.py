from discord_webhook import DiscordWebhook

webhook_url='https://discordapp.com/api/webhooks/529900505401393155/cb6JTsL_DDhsqbkgUyyqFOskAo3K0XOBWS8JwfC-ZcCat-M8qjxKpQqfulTs4jJsINdV'
webhook = DiscordWebhook(url=webhook_url, content='hi')
webhook.execute()




