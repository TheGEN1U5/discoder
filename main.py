import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import json
from workflows import *
from fetchgit import *

import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Dictionary to store conversation states
user_states = {}

class ConversationState:
    def __init__(self):
        self.step = 0
        self.answers = {}

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='createproject')
async def startproject(ctx, name):
    channel_name = "discoder-" + name.replace(" ", "-").lower()
    proj = await ctx.guild.create_text_channel(channel_name)
    await proj.send(f"Okay, let's intialize the project: {name}")

    #asking question
    user_id = ctx.author.id
    user_states[user_id] = ConversationState()
    success = await ask_question(ctx, proj)
    if success == -1:
        await proj.send("deleting channel...")
        await asyncio.sleep(5)
        await proj.delete()

async def ask_question(ctx, proj):
    user_id = ctx.author.id
    state = user_states[user_id]
    
    questions = [
        {
            "content": "Please enter the Public GitHub repository link of your project: links only",
            "key": "github"
        },
        {
            "content": "What techstack or technology do you use in the project? Descriptive answer",
            "key": "stack"
        }
    ]
    
    if state.step < len(questions):
        await proj.send(questions[state.step]["content"])
        
        def check(m):
            return m.author == ctx.author and m.channel == proj
        
        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            state.answers[questions[state.step]["key"]] = msg.content
            state.step += 1
            await ask_question(ctx, proj)
        except asyncio.TimeoutError:
            await proj.send("You took too long to respond!")
    else:
        success = await create_proj(proj, state.answers)
        return success

async def create_proj(proj, answers):
    # create projects/id directory
    proj_name = proj.name.replace("-", "_")
    readmesum = ""
    try:
        # Your existing code
        readmesum = await readme_summariser(
            await fetch_files(answers["github"], "README.md")
        )
    except Exception as e:
        await proj.send(f"Error: {str(e)}")
    try:
        os.makedirs(f"projects/{proj.guild.id}/{proj_name}")
        # add last_edited
        proj_dict = {
            "name" : proj_name,
            "parent": proj.id,
            "github": answers["github"],
            "stack": answers["stack"],
            "summary": readmesum,
            "discussions": []
        }
        with open(f"projects/{proj.guild.id}/{proj_name}/{proj_name}.json", "w") as f: 
            json.dump(proj_dict, f, indent=4)
        await proj.send("```json\n" + str(proj_dict) + "\n```\n")
    except FileExistsError:
        await proj.send("Project with same name already exists in this channel", str(e))
        return -1

    
    # put json file in directory

@bot.command(name='deleteproject')
async def deleteproject(ctx):
    proj_name = ctx.channel.name.replace("-", "_")
    proj_dir = f"projects/{ctx.guild.id}/{proj_name}"
    await ctx.send("deleting project...")
    await ctx.send("deleting files...")
    try:
        for file in os.listdir(proj_dir):
            os.remove(f"{proj_dir}/{file}")
        os.rmdir(f"{proj_dir}")
    except OSError:
        await ctx.send(f"no such project {proj_name}")
    await ctx.send("deleting channel...")
    await asyncio.sleep(2)
    await ctx.channel.delete()

@bot.command()
async def startdiscussion(ctx, name):
    proj_name = ctx.channel.name.replace("-", "_")
    proj_dir = f"projects/{ctx.guild.id}/{proj_name}"
    message = await ctx.send(f"Okay, let's start working on {name}")
    thread = await message.create_thread(name=f"New discussion: {name}")
    await thread.send("hello there you can start your discussion now. I'll quietely monitor it in the background.")
    

@bot.command(name='enddiscussion')
async def end_discussion(ctx):
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("This command can only be used in a thread.")
        return 0
    proj_name = ctx.channel.parent.name.replace("-", "_")
    proj_dir = f"projects/{ctx.guild.id}/{proj_name}"
    # getting messages
    conversation = ""
    async for message in ctx.channel.history(limit=None, oldest_first=True):
        if (message.content != "?enddiscussion" and not message.author.bot):
            conversation += f"{message.author.display_name}:\t{message.content}\n"
    discussion_summary = discussion_summariser(conversation)
    await ctx.send(f"Here is what I understood from your conversation:\n```{discussion_summary}```")
    await ctx.send("What else would you like to add more?")
    def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")
    discussion_summary += msg.content
    await ctx.send(f"Final summary:\n ```{discussion_summary}```")
    discussion = {
        "id": ctx.channel.id,
        "name": proj_name,
        "conversation": discussion_summary
    }
    with open(f"{proj_dir}/{proj_name}.json", "r+") as f:
        data = json.load(f)
        data["discussions"].append(discussion)
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate() 

bot.run(TOKEN)