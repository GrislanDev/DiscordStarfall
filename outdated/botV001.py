"""
Discord Bot as UI for Starfall. Currently compatible with mainV003.

Features:
- !start command is stable
- !lore command is stable
"""

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

from mainV003 import *

Client = discord.Client()
bot_prefix= "?"
client = commands.Bot(command_prefix=bot_prefix)

world = World("saves\\testBot.json")

print ("Set up complete.")

def alphanumeric(s):
    """ Returns if <str> s only contains letters and numbers. """
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for ch in s:
        if not(ch in allowed):
            return False
    return True

def hasAccount(author):
    """ Returns if player already has an account to play with. """
    return (str(author) in world.info["accounts"].keys())
    
@asyncio.coroutine
def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith("!"):
        content = message.content.split()
        parts = len(content)

        if content[0] == "!start":
            if parts == 2:
                if hasAccount(message.author):
                    # Player musn't already have an account
                    yield from client.send_message(
                        message.channel,
                        "You already have the faction '{}'. There is a limit to one faction per user.".format(world.info["accounts"][str(message.author)])
                        )
                elif content[1] in world.info["players"].keys():
                    # Player name musn't already be taken
                    yield from client.send_message(message.channel,"That faction name's taken already. Please enter another.")
                elif not(alphanumeric(content[1])):
                    # Player name must be alphanumeric
                    yield from client.send_message(message.channel,"Faction names must be alphanumeric. Please enter another.")
                else:
                    # Name works, create new player
                    world.info["accounts"][str(message.author)] = content[1]
                    newPlayer(content[1], world)
                    world.save_all()
                
                    yield from client.send_message(message.channel,"Welcome to Starfall, {}.".format(content[1]))
            else:
                yield from client.send_message(message.channel,"The syntax is: '!start factionName'\n Enter '!help' for more info.")
        elif content[0] == "!lore":
            yield from client.send_message(
                message.channel,
                """In the Revelation we discovered and decrypted the Nexon, an ancient technology holding the secrets to galatical exploration.
In the Expansion we left our ravished Solar System and colonized the far reaches of another galaxy.

Those were days of peace and cooperation, when stability was maintained by the Council and protected by the Warlocks.

In the Stagnation our resources ran thin as our populations rocketed. Unrest grew as the Council turned corrupt and locked away the Nexon for themselves.
In the Fall our Warlocks turned us against each other, and our galaxy plummeted into chaos.

Those were days of despair and betrayal, a pathetic repetition of our destruction of the Milky Way.

Those days are over.

We have entered the Resurrection. The Citadel of Epsilus stole the Nexon and destroyed it.
The Warlocks have been exiled to the Deep Rim, now replaced by Factions who once knelt beneath them.
Lead yours wisely, {}. Many threats await your coming.

The Warlocks now plot for a return to the Fall, and will strike against any sign of unity.
The Factions all vie for the control of the galaxy, and will do whatever it takes to get there.

Welcome to Starfall.
""".format(str(message.author)))          

client.run("MzMxOTE2MTcxODE1NDE5OTA0.DEQc4Q.jG-nnl3Di0VJmJyZbaDFE38XbGk")
