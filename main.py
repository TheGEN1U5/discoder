import discord
from discord.ext import commands
import asyncio
import json
from workflows import *
from fetchgit import *
from token_checker import token_checker
import os
from helperf import split_preserve_format
# import logging

# # remove duplicate logging
# logging.basicConfig(level=logging.WARNING)  # Suppress INFO logs from root logger
# discord_logger = logging.getLogger('discord')
# discord_logger.propagate = False  # Prevent passing logs to root logger

tokens = token_checker()
if not tokens[0]:
	print("Please enter your Discord token manually in your .env file.")
	__import__('sys').exit(1)

discord_token = tokens[1]


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
async def startproject(ctx, name: str = None):

    if name is None:
        await ctx.send("Please enter a name for the project as an argument after the command.")
        await ctx.send("Usage:\n `?createproject [name_of_the_project]`")
        return

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

@startproject.error
async def startproject_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Usage: `!createproject <project_name>` - Please provide a project name.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Make sure the project name is a valid string.")
    else:
        await ctx.send(f"An unexpected error occurred: {error}")

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
            msg = await bot.wait_for('message', check=check, timeout=180.0)
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
        readmesum = readme_summariser(
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
        await proj.send(proj_dict["summary"])
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
    await thread.send("hello there you can start your discussion now. I'll quietly monitor it in the background.")
    

@bot.command(name='enddiscussion')
async def end_discussion(ctx):
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("This command can only be used in a thread.")
        return
    global proj_name 
    global proj_dir
    proj_name = ctx.channel.parent.name.replace("-", "_")
    proj_dir = f"projects/{ctx.guild.id}/{proj_name}"
    new_discussion = await update_json(ctx, await extract_messages(ctx))
    with open(f"{proj_dir}/{proj_name}.json", "r") as f:
        github_link = json.load(f)["github"]
    await ctx.send("### Hold tight!\nWe are converting your conversations to code")
    tree = await fetch_directory_tree(github_link)
    await ctx.send("...")
    files = files_summariser(tree, new_discussion["dict"])
    await ctx.send("...")
    repo_content = await fetch_files(github_link, set(files))

    await ctx.send("...")
    codeblock = codeblock_creator(tree, repo_content, new_discussion["dict"])
    await ctx.send("...")
    # print(codeblock)
    await ctx.send("...")
    await ctx.send("# Suggested Solutions:")
    await send_chunked(ctx, codeblock)
    
# getting messages
async def extract_messages(ctx):
    conversation = ""
    async for message in ctx.channel.history(limit=None, oldest_first=True):
        if (message.content != "?enddiscussion" and not message.author.bot):
            conversation += f"{message.author.display_name}:\t{message.content}\n"
    discussion = discussion_summariser(conversation)
    await ctx.send(f"## Here is what I understood from your conversation:")
    await ctx.send(discussion[1])
    return discussion

# updating project json file 
async def update_json(ctx, discussion):
    new_discussion = {
        "id": ctx.channel.id,
        "name": proj_name,
        "summary": discussion[1],
        "dict": discussion[0]
    }
    with open(f"{proj_dir}/{proj_name}.json", "r+") as f:
        data = json.load(f)
        data["discussions"].append(new_discussion)
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()
    return new_discussion

async def send_chunked(ctx, content):
    """Sends messages in chunks with proper error handling"""
    for chunk in split_preserve_format(content, 1999):
        try:
            await ctx.send(chunk)
        except discord.HTTPException as e:
            await ctx.send(f"Error sending message: {e}")
    

bot.run(discord_token)
