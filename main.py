import discord
from discord.ext import commands
from dotenv import load_dotenv

import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@bot.command()
async def add(ctx, left: int, right: int):
    print("here");
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def say(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def startproject(ctx, name):
    message = await ctx.send(f"Okay, let's start working on {name}")
    thread = await message.create_thread(name=f"New discussion: {name}")
    await thread.send("hello there you can start your discussion now. I'll quietely monitor it in the background.")

@bot.command(name='enddiscussion')
async def end_discussion(ctx):
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("This command can only be used in a thread.")
        return
    # getting messages
    conversation = ""
    
    async for message in ctx.channel.history(limit=None, oldest_first=True):
        if (message.content != "?enddiscussion" and not message.author.bot):
            conversation += f"{message.author.display_name}:\t{message.content}\n"
    await ctx.send(f"recorded conversation is:\n```{conversation}```")

bot.run(TOKEN)