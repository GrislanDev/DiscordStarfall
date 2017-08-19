"""
Discord Bot as UI for Starfall. Currently compatible with mainV008.

Features:
    start, lore, upgrade, build, train commands stable
    infoo, infof commands tested for full-info (limited-info case needs testing)
"""

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

from mainV009 import *
import text

Client = discord.Client()
bot_prefix= "$"
client = commands.Bot(command_prefix=bot_prefix)

world = World("saves\\ZortanTest.json")
command_info = text.command_info
tut_info = text.tut_info

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

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(bot_prefix):
        content = message.content.split()
        parts = len(content)
        start = content[0][1:]

        world.update_time()

    #===================================================== INFORMATION COMMANDS HERE =====================================================

        if start == "help":
            if parts == 1:
                t = "***==== AVAILIBLE COMMANDS ====***\n"
                for command in sorted(command_info):
                    t += "*{0}* : {1}\n\n".format(command, command_info[command][1])
                yield from client.send_message(message.channel, t)
            elif parts == 2:
                if content[1] in command_info:
                    command = content[1]
                    t = "***==== {0} COMMAND INFO ====*** \nPurpose: {1}\nSyntax: {2}\n".format(command.upper(), command_info[command][1], command_info[command][0])
                    yield from client.send_message(message.channel, t)
                else:  
                    yield from client.send_message(message.channel, "That command doesn't exist. To see a list of commands, type '$help'.")
            else:  
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["help"][0]))

        if start == "tut":
            if parts == 1:
                t = "***==== AVAILIBLE TOPICS ====***\n"
                for topic in sorted(tut_info):
                    t += topic + ", "
                t = t[:-2]
                yield from client.send_message(message.channel, t)
            elif parts == 2:
                if content[1] in tut_info:
                    t = tut_info[content[1]]
                    yield from client.send_message(message.channel, t)
                else:  
                    yield from client.send_message(message.channel, "That topic doesn't exist. To see a list of topics, type '$tut'.")
            else:  
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["tut"][0]))

        if start == "start":
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
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["start"][0]))

        elif start == "infoo":
            if parts == 2:
                if content[1] in world.info["outposts"]:
                    # Outpost must exist
                    outpost = world.info["outposts"][content[1]]
                    yield from client.send_message(
                        message.channel,outpost.information(hasAccount(message.author) and outpost.owner == world.info["accounts"][str(message.author)])
                        )
                else:
                    yield from client.send_message(message.channel,"No information found. The outpost '{}' does not exist.".format(content[1]))
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["infoo"][0]))

        elif start == "infof":
            if parts == 1 and hasAccount(message.author):
                yield from client.send_message(message.channel,world.info["players"][world.save["accounts"][str(message.author)]].information())
            elif parts == 2:
                if content[1] in world.info["players"]:
                    player = world.info["players"][content[1]]
   
                    yield from client.send_message(
                        message.channel,player.information(hasAccount(message.author) and world.info["accounts"][str(message.author)] == content[1])
                        )
                else:
                    yield from client.send_message(message.channel,"No information found. The faction '{}' does not exist.".format(content[1]))
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["infof"][0]))

        elif start == "infou":
            if parts > 1:
                content[1] = message.content[message.content.index(" ")+1:]
                if hasAccount(content[1]):
                    yield from client.send_message(
                        message.channel,world.info["players"][world.info["accounts"][content[1]]].information(content[1]==world.info["accounts"][str(message.author)])
                        )
                else:
                    yield from client.send_message(message.channel,"No information found. {} does not have a faction.".format(content[1]))
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["infou"][0]))

        elif start == "flist":
            t = "***==== ALL FACTIONS ====***\n"
            for p in sorted(world.info["players"].keys()):
                t += p + ", "
            t = t[:-2]
            t += "\n"
            yield from client.send_message(message.channel,t)

        elif start == "olist":
            t = "***==== ALL OUTPOSTS ====***\n"
            for o in sorted(world.info["outposts"].keys()):
                t += o + ", "
            t = t[:-2]
            t += "\n"
            yield from client.send_message(message.channel,t)
           
        elif start == "lore":
            yield from client.send_message(
                message.channel,text.lore["main"].format(str(message.author)))

        #===================================================== OUTPOST COMMANDS HERE =====================================================
            
        elif start == "upgrade":
            if parts == 2:
                if hasAccount(message.author):
                    if content[1] in world.info["players"][world.save["accounts"][str(message.author)]].outposts:
                        result = world.info["outposts"][content[1]].upgrade()
                        world.save_all()
                        yield from client.send_message(
			    message.channel, result
			    )
                        
                    else:
			# Player must own outpost
                        yield from client.send_message(
			    message.channel, "Sorry, you do not control the outpost '{}'.".format(content[1])
			    )
                else:
		    # Player must have an account to play
                    yield from client.send_message(
			message.channel, 
			"Sorry, you must start an account to play! Type '$start' to begin."
			)
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["upgrade"][0]))
                
        elif start == "build":
            if parts == 4:
                if hasAccount(message.author):
                    result = world.info["players"][world.save["accounts"][str(message.author)]].buildOutpost(
                                content[1], content[2], content[3]
                                )
                    world.save_all()
                    yield from client.send_message(message.channel,result)
                    
                else:
                    yield from client.send_message(message.channel,"Sorry, you must start an account to play! Type '$start' to begin.")
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["build"][0]))

        #===================================================== BATTLE COMMANDS HERE =====================================================

        elif start == "train":
            if parts == 3:
                if hasAccount(message.author):
                    result = world.info["players"][world.save["accounts"][str(message.author)]].train(
                                content[1], content[2]
                                )
                    world.save_all()
                    yield from client.send_message(message.channel, result)
                else:
                    yield from client.send_message(message.channel,"Sorry, you must start an account to play! Type '$start' to begin.")
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["train"][0]))

        elif start == "reinforce":
            if parts == 4:
                if hasAccount(message.author):
                    result = world.info["players"][world.save["accounts"][str(message.author)]].reinforce(
                                content[1], content[2], content[3]
                                )
                    world.save_all()
                    yield from client.send_message(message.channel, result)
                else:
                    yield from client.send_message(message.channel,"Sorry, you must start an account to play! Type '$start' to begin.")
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["reinforce"][0]))

        elif start == "strike":
            if parts == 4:
                if hasAccount(message.author):
                    result = world.info["players"][world.save["accounts"][str(message.author)]].strike(
                                content[1], content[2], content[3]
                                )
                    world.save_all()
                    yield from client.send_message(message.channel, result)
                else:
                    yield from client.send_message(message.channel,"Sorry, you must start an account to play! Type '$start' to begin.")
            else:
                yield from client.send_message(message.channel, "The syntax is {}. Type '$help' for more info.".format(command_info["strike"][0]))

                    
        #===================================================== SOCIAL COMMANDS HERE =====================================================
   
client.run("MzMxOTE2MTcxODE1NDE5OTA0.DEQc4Q.jG-nnl3Di0VJmJyZbaDFE38XbGk")
