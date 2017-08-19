#MzMxOTE2MTcxODE1NDE5OTA0.DEQc4Q.jG-nnl3Di0VJmJyZbaDFE38XbGk

"""
Bot as UI to interact with mainV002.

Features:

Goals:

help <commandName>
start <factionName>

"""

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
Client = discord.Client()
bot_prefix= "?"
client = commands.Bot(command_prefix=bot_prefix)

@asyncio.coroutine
def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith("lol"):
        yield from client.send_message(message.channel, "me 2 bro {}".format(str(message.author)))
    elif message.content.startswith("donate"):
        yield from client.send_message(message.channel, str(message.content.split()))

client.run("MzMxOTE2MTcxODE1NDE5OTA0.DEQc4Q.jG-nnl3Di0VJmJyZbaDFE38XbGk")
