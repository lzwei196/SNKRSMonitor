from discord_webhook import DiscordWebhook
from time import sleep

def notifyDisc(data):
    sleep(0.3)
    webhook_url='https://discordapp.com/api/webhooks/533835559043334165/T6hSuZahCvNPkuXqhDO7KStIhfif5LhXtVMDhl1VZP5xkEKvSMKwhGNte7657lF10DSk'
    webhook = DiscordWebhook(url=webhook_url, content=data)
    webhook.execute()


def printf(*args):
    vals = list(args)
    print(vals)
    for i in range(len(vals)):
        vals[i] = vals[i].encode('utf-8')
    print(*vals)

notifyDisc('https://www.nike.com/launch/t/sb-dunk-high-pro-black-hornet/')