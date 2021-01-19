import discord
from discord.ext import commands
import random
import sqlite3

PREFIX = "!"
client = commands.Bot(command_prefix = "!")

db = sqlite3.connect("build.sql")

@client.command()
async def on_ready():
    print("Bot is ready")

@client.command()
async def on_member_join(member):
    db.execute("INSERT INFO exp (UserID) VALUES (?), member.id")

@client.event
async def process_xp(message):
    xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)
    await add_xp(message, xp, lvl)

async def add_xp(message,xp, lvl):
    xp_to_add = random.randint(1,15)
    new_lvl = int(((xp + xp_to_add)//42)** 0.55)
    print(f"{xp_to_add} {new_lvl} = ")

    db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock  = ? WHERE UserID = ?", xp_to_add, new_lvl, message.author.id)
        
    if new_lvl > lvl:
        await message.channel.send(f"{message.author.mention} You reached level {new_lvl:,}")

@client.event
async def on_message(message):
    if not message.author.bot:
        await process_xp(message) 

client.run("TOKEN")
