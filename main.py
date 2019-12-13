# External modules.
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Internal modules.
from modules.quote import *
from modules.reminder import *
from modules.uwulate import *
from utilities.logger import *

# Load the required variables from .env file.
load_dotenv()
env_token = os.getenv('DISCORD_TOKEN')

# Instantiate a client and run it.
bot = commands.Bot(command_prefix='!')

# ------------------ EVENTS START HERE ------------------ #

@bot.event
async def on_ready():
    print(f'[{timestamp()}] Logged in as {bot.user}!')

@bot.event
async def on_message(message):

    # Stops bot from trigger responses to its own messages.
    if message.author == bot.user:
        return

    # Log the message in console, change output to log file later.
    log(f'[{timestamp()}] Message from {message.author}: {message.content}')

    # Hidden feature.
    if message.content.find('bitch') >= 0: 
        await message.channel.send(message.author.name + ', you kiss your mother with that mouth?')

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the permission to use this command.')
    
@bot.event
async def on_reaction_add(reaction, user):

    # Representations of emojis.
    asterisk_emoji = b'*\xef\xb8\x8f\xe2\x83\xa3'
    wheelchair_emoji = b'\xe2\x99\xbf'

    # Triggers the quote module.
    if(reaction.emoji.encode() == asterisk_emoji):
        log(f'[{timestamp()}] {user.name} quoted message: {reaction.message.content}')
        await quoteMessage(reaction, user)
        await reaction.message.remove_reaction(asterisk_emoji.decode(), user)

    # Triggers the uwulating module.
    if(reaction.emoji.encode() == wheelchair_emoji):
        log(f'[{timestamp()}] {user.name} uwulated message: {reaction.message.content}')
        await uwulateMessage(reaction, user, bot)
        await reaction.message.remove_reaction(wheelchair_emoji.decode(), user)

# ------------------ COMMANDS START HERE ------------------ #

# Mirrors whatever the user says, sends it back to you as a PM.
@bot.command(name='mirror')
async def mirror(ctx):
    member = ctx.message.author
    response = ctx.message.content.split()[1:]
    response = ' '.join(response)
    await member.create_dm()
    await member.dm_channel.send(response)

# Reminder feature, like the one on Reddit.
@bot.command(name='remindme')
async def reminder(ctx):
    await set_reminder(ctx)

# uwutranslator, but no source code.
@bot.command(name='uwulate')
async def uwu(ctx):
    message = uwulate(ctx.message.content.split(' ', 1)[1])
    await ctx.message.channel.send(message)

# Run the bot.
bot.run(env_token)