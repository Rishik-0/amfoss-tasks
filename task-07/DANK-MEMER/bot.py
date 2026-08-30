import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from database.users import add_user
from database.db import initialize_database
from database.shop import initialize_items
from database.users import getdb_balance
from database.users import db_setsail
from database.users import db_trade
from commands.onepiece import get_logpose
from database.users import db_worstgeneration
from database.shop import get_all_items
from database.shop import buy_item

from database.shop import get_inventory
from database.users import db_raid

import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w' )
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():

    print(f"{bot.user.name},Bot is currently online")

@bot.event
async def on_member_join(member):
    add_user(member.id,member.name)
    print(f"{member.name} has joined the server!")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello Pirate{ctx.author.mention}!")

@bot.command()
async def bounty(ctx):
    balance = getdb_balance(ctx.author.id)
    await ctx.send(f"Balance berries: {balance}")

@bot.command()
async def setsail(ctx):
    curr_time = time.time()
    result = db_setsail(ctx.author.id, curr_time)
    await ctx.send(result)

@bot.command()
async def trade(ctx, member: discord.Member, number: int):
    if ctx.author == member:
        await ctx.send("You cannot tradde with yourself!")
    elif number < 0:
        await ctx.send("Number of berries should be positive!")
    else:
        res = db_trade(ctx.author.id, member, number)
        if res == "Trade Complete!":
            await ctx.send(res)
            await ctx.send(f"{member.mention} just received {number} berries!!")
        else:
            await ctx.send(res)


@bot.command()
async def logpose(ctx):
    choice, name, desc = await get_logpose()
    if choice == 0:
        await ctx.send(f"Name: {name}\n Bounty: {desc}")
    elif choice == 1:
        await ctx.send(f"Fruit: {name}\n Power: {desc}")


@bot.command()
async def worstgeneration(ctx):
    res = db_worstgeneration()
    await ctx.send(f"****The Worst Generation Leaderboard****")
    for i in res:
        await ctx.send(f"Username: {i[0]}, Berries: {i[1]}")

@bot.command()
async def shop(ctx):
    res = get_all_items()
    
    message = "BERRY BROCKERS SHOP!\n\n"
    for item in res:
        message+=f"Item Id: {item[0]}. {item[1]} \t Price: {item[2]} Berries \t Effect: {item[4]} \n Description: {item[3]}\n\n "
    await ctx.send(message)


@bot.command()
async def buy(ctx,item_id: int):
    result = buy_item(ctx.author.id, item_id)
    await ctx.send(result)

@bot.command()
async def inventory(ctx):
    res = get_inventory(ctx.author.id)
    
    if not res:
        await ctx.send("Your inventory is empty!")
        return

    message = f"{ctx.author.name.upper()}'S INVENTORY!\n\n"

    for item in res:
        message += f"Item: {item[0]} \t Status: {item[2]} \n Description: {item[1]}\n\n"
    await ctx.send(message)

@bot.command()
async def raid(ctx, member: discord.Member):

    if ctx.author == member:
        await ctx.send("You cannot raid yourself!")

    else:
        result = db_raid(ctx.author.id, member)
        await ctx.send(result)

initialize_database()
initialize_items()
add_user(816992763223867424, "rishik_raj")
bot.run(token, log_handler=handler, log_level=logging.DEBUG)