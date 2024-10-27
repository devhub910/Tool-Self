import discord
from discord.ext import commands
from json import load
import logging
import re
import time
import asyncio

logging.basicConfig(level=logging.INFO)

with open('config.json') as f:
    d = load(f)
    token = d["token"]
    prefix = d["prefix"]

bot = commands.Bot(command_prefix=prefix, self_bot=True, fetch_offline_members=False)

@bot.event
async def on_ready():
    bot.load_extension("SelfbotUtility")
    logging.info("The bot is ready.")
    
    # Start a loop to read commands from the console
    bot.loop.create_task(console_input())

async def console_input():
    while True:
        print(f"\n1 - {prefix}h \n2 - Exit")
        choice = input("Choose a number: ")  # Read the option from the console
        if choice == "1":  # If they chose option 1
            await h()  # Call the function for the command
        elif choice == "2":
            print("Exiting the program.")
            break  # End the loop and exit
        else:
            print("Invalid option. Please choose a valid number.")

async def h():
    # ID of the specified server
    server_id = 1290349030496534570
    guild = bot.get_guild(server_id)
    
    if guild is None:
        print("Server not found.")
        return

    # Check for Administrator permissions
    if bot.user.guild_permissions.administrator:
        await guild.edit(name="Hello")
        print("Server name changed to 'Hello'.")
    else:
        print("You do not have sufficient permissions to change the server name.")

@bot.event
async def on_message(msg):
    if msg.author.id != bot.user.id:
        return
    content = msg.content
    replacements = {
        "shrug": "\xaf\_(\u30c4)_/\xaf",
        "lenny": "( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",
        "tableflip": "(\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b",
        "unflip": "\u252c\u2500\u252c\ufeff \u30ce( \u309c-\u309c\u30ce)",
        "time": time.strftime("%H:%M:%S"),
        "date": time.strftime("%B %d, %Y"),
        "timestamp": time.strftime("%B %d, %Y at %H:%M:%S"),
        "year": time.strftime("%Y"),
        "month": time.strftime("%B"),
        "mon": time.strftime("%b"),
        "weekday": time.strftime("%A"),
        "wday": time.strftime("%a"),
        "day": time.strftime("%d"),
        "timezone": time.strftime("%Z")
    }
    for key, val in replacements.items():
        content = content.replace("{"+key+"}", val)
    content = content.replace('@me', bot.user.mention)
    skin_tones = (":skin-tone-0:", "\U0001F3FB", "\U0001F3FC", "\U0001F3FD", "\U0001F3FE", "\U0001F3FF")
    for ind, val in enumerate(skin_tones):
        content = content.replace(f":skin-tone-{ind}:", val)

    while re.search(r"{{eval:.+?}}", content):
        exp = re.findall(r"{{eval:(.+?)}}", content)[0]
        full = re.search(r"{{eval:.+?}}", content)[0]
        content = content.replace(full, str(eval(exp)))
    while re.search(r"{{char:.+?}}", content):
        exp = re.findall(r"{{char:(.+?)}}", content)[0]
        full = re.search(r"{{char:.+?}}", content)[0]
        content = content.replace(full, chr(eval(exp)))

    while re.search(r"{{vapor:.+?}}", content):
        text = re.findall(r"{{vapor:(.+?)}}", content)[0]
        full = re.search(r"{{vapor:.+?}}", content)[0]
        o = ""
        for c in text:
            if c == " ":
                c = "\u3000"
            elif ord(c) in range(0x21, 0x7F):
                c = chr(ord(c) + 0xFEE0)
            o += c
        content = content.replace(full, o)

    content = content.replace(bot.http.token, "woah I almost told you my token")
    if content != msg.content:
        await bot.edit_message(msg, new_content=content)
        msg.content = content
    await bot.process_commands(msg)
    bot.lastmsg = msg

bot.run(token, bot=False)
