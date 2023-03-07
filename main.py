version = 0.3
dev = "! chikn#0556"

import discord
import json
import os
import colorama
import datetime

from colorama import Fore
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)
token = config.get("Token")
prefix = config.get("Prefix")
starttime = datetime.datetime.utcnow()

client = commands.Bot(self_bot=True, command_prefix=prefix, case_insensitive=True,)
client.remove_command("help")

@client.event
async def on_ready():
    print(f'{Fore.CYAN}Swift Helper Beta {version} - Logged Into: {client.user} ID: {client.user.id}')

@client.event
async def on_command(ctx):
    print(f"{Fore.CYAN}Swift Helper | {Fore.RESET}Command used - {ctx.command.name}")

@client.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**Help Menu**\n> `{prefix}swift - sends swift help menu`\n> `{prefix}selfbot - sends selfbot help menu`\n")

@client.command()
async def swift(ctx):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**Swift Menu**\n> `{prefix}endticket [@user] - ends ticket with a nice message`\n> `{prefix}recovery - tells user how to recover vouches`\n> `{prefix}recoverycomplete [Id's] - notifies Swift admin on completed recovery`\n> `{prefix}antispam [@user] - tells user how to appeal server blacklist`\n> `{prefix}invalidproof [@user] - tells user how to send validproof`\n> `{prefix}recoveryproccess [id] - does recovery proccess automatically`\n")

@client.command()
async def selfbot(ctx):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**Selfbot Menu**\n> `{prefix}credits - credits for Swift Helper`\n> `{prefix}uptime - uptime for swift helper`\n> `{prefix}servericon - sends server icon`\n> `{prefix}whois [user] - sends user info`\n> `{prefix}serverinfo - sends guild info`\n> `{prefix}av [user] - sends users pfp`\n")

@client.command()
async def endticket(ctx, user):
    await ctx.message.delete()
    await ctx.send(f"{user} \n \n**Seems like this ticket has been completed**\n \n> `Sadly this means are time together is coming to a end.`\n> `if you need any more support you know where to find us.`\n \nIf that is all have a **Swiftful Day!**")

@client.command()
async def recovery(ctx):
    await ctx.message.delete()
    await ctx.send("**Provide proof for the above vouches to prove that you were the owner of the account **\n \n**Proof Allowed Is Below**\n> `Payment Proof`\n> `Chat/ticket Logs`\n> `Uncropped Screenshots ONLY!`\n \nYou have **12 Hours** to respond or the ticket will be closed..")

@client.command()
async def recoverycomplete(ctx, id1, id2):
    await ctx.message.delete()
    await ctx.send(f"**{id1}** `>>` **{id2}**\n \n**Provided Proof**\n> `Payment Proof:`:white_check_mark:\n \n<@&888763368943534101>")

@client.command()
async def antispam(ctx, user):
    await ctx.message.delete()
    await ctx.send(f"{user}\n \n**Hello, it seems your server has been blacklisted due to new anti-spam rules we have added. If you feel like this is unjustified you may appeal the blacklist.**\n \n**Appeal Instructions**\n> `Go to` #📝┃appeal-your-mark\n> `Open a ticket under server ban `\n \nSorry for the Inconvenience have a **Swiftful Day! **")

@client.command()
async def invalidproof(ctx, user):
    await ctx.message.delete()
    await ctx.send(f"{user}\n \n**Hello, it seems like the proof you have given is invalid to us.**\n \n**Submit Correct Proof As**\n> `Uncropped Screenshots of chat/ticket log`\n> `Uncropped screenshots of you receiving/sending funds`\n> `Link to ticket log`\n \nHopefully this corrects your mistakes, Thankyou.")

@client.command()
async def recoveryproccess(ctx, userid):
    await ctx.message.delete()
    await ctx.send(f"=add {userid}")
    try:
        user = client.get_user(int(userid))
        await user.send("**Hello, it seems another user is trying to recover from your account if this isnt you, you have 12 hours to respond to the ticket.**\n \nTicket Here - discord.gg/scammeralert\n \n- ScammerAlert staff")
    except:
        await ctx.send(f"**Could Not Send Dm To User ID:** `{userid}`")
    await ctx.send(f"+vouches {userid}")

# random command not needed to be added but why not. why am i still typing i need to stop pls help.

@client.command()
async def credits(ctx):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**Credits**\n> `Owner & Dev - {dev}`\n> `User & Lover - {client.user}`")

@client.command()
async def uptime(ctx):
    await ctx.message.delete()
    uptime = datetime.datetime.utcnow() - starttime
    uptime = str(uptime).split('.')[0]
    await ctx.send(f"```Swift Helper```\n**Uptime**\n> `{uptime}`")

@client.command()
async def servericon(ctx):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**{ctx.guild.name}'s Server Icon**\n> ||{ctx.guild.icon_url}||")

@client.command()
async def whois(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**User Name**\n> `{user.name}#{user.discriminator}`\n**User ID**\n> `{user.id}`\n**Created At**\n> `{user.created_at}`\n**User Avatar Url**\n> `{user.avatar_url}`\n")

@client.command()
async def serverinfo(ctx):
    await ctx.message.delete()
    guild = ctx.message.guild
    await ctx.send(f"```Swift Helper```\n**Server Name**\n> `{guild.name}`\n**Server ID**\n> `{guild.id}`\n**Server Owner Info**\n> **Username:** `{guild.owner}`\n> **ID:** `{guild.owner_id}`\n**Created At**\n> `{guild.created_at}`\n**Server Icon Url**\n> `{ctx.guild.icon_url}`\n")

@client.command()
async def av(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**{user}'s Avatar**\n> {user.avatar_url}")

try:
    client.run(token)
except discord.errors.LoginFailure:
    print(f"{Fore.CYAN}Swift Helper | {Fore.RED}ERROR: TOKEN IS INVALID!\n{Fore.RESET}Please put a valid token into config.json.\nTo get your token follow the tutorial here! https://www.youtube.com/watch?v=UN-8hBoDJYw")
    os.system('pause >NUL')