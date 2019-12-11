import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from modules.quote import *

# Load the required variables from .env file.
load_dotenv()
env_token = os.getenv('DISCORD_TOKEN')
env_guild = os.getenv('DISCORD_GUILD')

# Instantiate a client and run it.
bot = commands.Bot(command_prefix='!')

# ------------------ EVENTS START HERE ------------------ #

@bot.event
async def on_ready():
    print('----------------------------------------')
    print('Logged in as {0.user}!'.format(bot))

    guild = discord.utils.find(lambda g: g.name == env_guild, bot.guilds)
    print('Connected to guild: {0.name} ({0.id})'.format(guild))

    members = '\n - '.join([member.name for member in guild.members])
    print('Guild Members:\n - ' + members)
    print('----------------------------------------')

@bot.event
async def on_message(message):

    # Stops bot from trigger responses to its own messages.
    if message.author == bot.user:
        return

    # Log the message in console, change output to log file later.
    print('Message from {0.author}: {0.content}'.format(message))

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

    # Triggers the quote module.
    if(reaction.emoji.encode() == asterisk_emoji):
        print("Reaction added to message: " + reaction.message.content)
        await quoteMessage(reaction, user)

# ------------------ COMMANDS START HERE ------------------ #

# Bot commands.
# Mirrors whatever the user says, sends it back to you as a PM.
@bot.command(name='mirror')
async def mirror(ctx):
    member = ctx.message.author
    response = ctx.message.content.split()[1:]
    response = ' '.join(response)
    await member.create_dm()
    await member.dm_channel.send(response)

# Run the bot.
bot.run(env_token)