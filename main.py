version = 0.4
dev = "! chikn#0556"

import discord
import json
import os
import colorama
import datetime
import requests
import ctypes

from colorama import Fore
from pystyle import Colors, Colorate
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
    ctypes.windll.kernel32.SetConsoleTitleW(f"Swift Helper | Beta {version} | Logged Into: {client.user} | Prefix: {prefix}")
    print(Colorate.Horizontal(Colors.blue_to_cyan,"""
  /$$$$$$  /$$      /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$$
 /$$__  $$| $$  /$ | $$|_  $$_/| $$_____/|__  $$__/
| $$  \__/| $$ /$$$| $$  | $$  | $$         | $$   
|  $$$$$$ | $$/$$ $$ $$  | $$  | $$$$$      | $$   
 \____  $$| $$$$_  $$$$  | $$  | $$__/      | $$   
 /$$  \ $$| $$$/ \  $$$  | $$  | $$         | $$   
|  $$$$$$/| $$/   \  $$ /$$$$$$| $$         | $$   
 \______/ |__/     \__/|______/|__/         |__/   
                                                                                                                                                  
""", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"Swift Helper Beta {version}\nLogged Into: {client.user} - ID: {client.user.id}", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan,"--------------------------------------------------"))

@client.event
async def on_command(ctx):
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"Swift Helper | Command used - {ctx.command.name}", 1))

# Help Commands!

@client.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send(f"# Swift Helper\n**Help Menu**\n> `{prefix}swift - sends swift help menu`\n> `{prefix}selfbot - sends selfbot help menu`\n")

@client.command()
async def swift(ctx):
    await ctx.message.delete()
    await ctx.send(f"# Swift Helper\n**Swift Menu**\n> `{prefix}sadeny [userid] [reason] - Tells user vouch was denied`\n> `{prefix}saaccept [userid] - Tells user vouch was accepted`\n> `{prefix}recovery - tells user how to recover vouches`\n> `{prefix}recoveryadmin [id 1] [id 2]- notifies Swift admin on completed recovery`\n> `{prefix}antispam [@user] - tells user how to appeal server blacklist`\n> `{prefix}invalidproof [@user] - tells user how to send validproof`\n> `{prefix}recoveryproc [id] - does recovery proccess automatically`\n> {prefix}recoverydone - Tellse user that recovery is almost completed.")

@client.command()
async def selfbot(ctx):
    await ctx.message.delete()
    await ctx.send(f"# Swift Helper\n**Selfbot Menu**\n> `{prefix}credits - credits for Swift Helper`\n> `{prefix}uptime - uptime for swift helper`\n> `{prefix}servericon - sends server icon`\n> `{prefix}whois [user] - sends user info`\n> `{prefix}serverinfo - sends guild info`\n> `{prefix}av [user] - sends users pfp`\n> `{prefix}calc [#] [+,-,x,/] [#] - calculator`\n> `{prefix}theme [dark/light] - changes discord theme`\n")

# Swift commands!

@client.command()
async def saaccept(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"**Your vouch has been approved!** :white_check_mark:\n \nIf you need anything else let me know, if not have a good day/night :slight_smile:\n \n{user.mention}")

@client.command()
async def sadeny(ctx, user: discord.User, reason):
    await ctx.message.delete()
    await ctx.send(f"**Your vouch has been Denied!** :no_entry_sign:\n \n**Vouch Denial Reason:**\n> `{reason}`\n \n{user.mention}")

@client.command()
async def recovery(ctx):
    await ctx.message.delete()
    await ctx.send("**Send valid payment proofs for the vouches given above**\n \nImportant points: \n> Send payment proofs with **date and time**\n> Payment proof screenshot must be **new**\n> You have **12 hours** to do this\n> Mention **vouch id** with **payment proof**\n \nHope that's clear enough!\nIf you have any other doubts feel free to ask me.\n \n**Please read this before asking any questions**")

@client.command()
async def recoveryadmin(ctx, id1, id2):
    await ctx.message.delete()
    await ctx.send(f"{id1} >> {id2}\n \n**Provided Proof**\n> `Payment Proof:`:white_check_mark:\n \n<@888763368943534101>")

@client.command()
async def recoverydone(ctx, id1, id2):
    await ctx.message.delete()
    await ctx.send(f"**Thank you for submitting your proofs!**\n \nWe will review them within the next **12 hours.**\n \nOnce they have been approved, __Admins will do your import of the vouch profile.__")

@client.command()
async def antispam(ctx, user):
    await ctx.message.delete()
    await ctx.send(f"{user}\n \n**Hello, it seems your server has been blacklisted due to new anti-spam rules we have added. If you feel like this is unjustified you may appeal the blacklist.**\n \n**Appeal Instructions**\n> `Go to` #📝┃appeal-your-mark\n> `Open a ticket under server ban `\n \nSorry for the Inconvenience have a **Swiftful Day! **")

@client.command()
async def invalidproof(ctx, user):
    await ctx.message.delete()
    await ctx.send(f"{user}\n \n**Hello, it seems like the proof you have given is invalid to us.**\n \n**Submit Correct Proof As**\n> `Uncropped Screenshots of chat/ticket log`\n> `Uncropped screenshots of you receiving/sending funds`\n> `Link to ticket log`\n \nHopefully this corrects your mistakes, Thankyou.")

@client.command()
async def recoveryproc(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"=add {user.id}")
    await ctx.send(f"<@{user.id}>")
    await ctx.send(f"+vouches {user.id}")
    await user.send(f"**Hello** {user.mention}\n \nA Swift-Recovery Ticket has been Made Claiming to be You, please Respond to the Ticket ASAP to Accept/Decline this Request.\nYou have **12 Hours** from this Message to Respond.\n \n*Failure to Respond may Result in a Loss of your Profile & Un-Intended Consequences . . .*\n \n**Ticket:** https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}")

# Selfbot Commands!

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
    await ctx.send(f"```Swift Helper```\n**Server Name**\n> `{guild.name}`\n**Server ID**\n> `{guild.id}`\n**Server Owner Info**\n> **Username:** `{guild.owner}`\n> **ID:** `{guild.owner_id}`\n**Created At**\n> `{guild.created_at}`\n**Members**\n> `{guild.member_count}`\n**Server Icon Url**\n> `{ctx.guild.icon_url}`\n")

@client.command()
async def av(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"```Swift Helper```\n**{user}'s Avatar**\n> {user.avatar_url}")

@client.command()
async def calc(ctx, number: int, math, number1: int):
    await ctx.message.delete()
    if math == "+":
        answer = number + number1
        await ctx.send(f"```Swift Helper```\n**Asnwer Has Been Calculated**\n> {answer}")
    if math == "-":
        answer = number - number1
        await ctx.send(f"```Swift Helper```\n**Asnwer Has Been Calculated**\n> {answer}")
    if math == "x":
        answer = number * number1
        await ctx.send(f"```Swift Helper```\n**Asnwer Has Been Calculated**\n> {answer}")
    if math == "/":
        answer = number // number1
        await ctx.send(f"```Swift Helper```\n**Asnwer Has Been Calculated**\n> {answer}")

@client.command()
async def theme(ctx, theme):
    headers={'authorization': token, "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36"}
    await ctx.message.delete()
    if theme == "dark":
        requests.patch("https://canary.discordapp.com/api/v9/users/@me/settings",headers=headers, json={'theme': "dark"})
        await ctx.send(f"```Swift Helper```\n**Discord Theme**\n> Dark Theme")
    if theme == "light":
        requests.patch("https://canary.discordapp.com/api/v9/users/@me/settings",headers=headers, json={'theme': "light"})
        await ctx.send(f"```Swift Helper```\n**Discord Theme**\n> Light Theme")

try:
    client.run(token)
except discord.errors.LoginFailure:
    print(f"{Fore.CYAN}Swift Helper | {Fore.RED}ERROR: TOKEN IS INVALID!\n{Fore.RESET}Please put a valid token into config.json.\nTo get your token follow the tutorial here! https://www.youtube.com/watch?v=UN-8hBoDJYw")
    os.system('pause >NUL')