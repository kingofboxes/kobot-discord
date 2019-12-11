# Imports for main.
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from quote import *

# Load the required variables from .env file.
load_dotenv()
env_token = os.getenv('DISCORD_TOKEN')
env_guild = os.getenv('DISCORD_GUILD')

# Instantiate a client and run it.
bot = commands.Bot(command_prefix='!')

# Custom events.
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

    if message.author == bot.user:
        return

    print('Message from {0.author}: {0.content}'.format(message))

    if message.content.find('bitch') >= 0: 
        await message.channel.send(message.author.name + ', you kiss your mother with that mouth?')

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_reaction_add(reaction, user):

    asterisk_emoji = b'*\xef\xb8\x8f\xe2\x83\xa3'

    # Only trigger a response if the asterisk emoji is being used.
    if(reaction.emoji.encode() == asterisk_emoji):
        print("Reaction added to message: " + reaction.message.content)
        await quoteMessage(reaction, user)
    

# Bot commands.
@bot.command(name='mirror')
@commands.has_role('Admin')
async def mirror(ctx):
    member = ctx.message.author
    response = ctx.message.content.split()[1:]
    response = ' '.join(response)
    await member.create_dm()
    await member.dm_channel.send(response)

@bot.command(name='hello')
async def hello(ctx):
    embed = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embed.add_field(name="Field1", value="hi", inline=False)
    embed.add_field(name="Field2", value="hi2", inline=False)
    await ctx.message.channel.send(embed=embed)

bot.run(env_token)