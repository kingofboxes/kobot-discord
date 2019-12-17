# External modules.
import os, discord, json, pytz
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime

# Internal modules.
from modules.quote import quoteMessage
from modules.reminder import set_reminder, showReminders
from modules.uwulate import uwulate, uwulateMessage
from modules.dictionary import get_definition_normal, get_definition_urban
from modules.dice import roll_dice
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
    check_reminders.start()

@bot.event
async def on_message(message):
    # Stops bot from trigger responses to its own messages.
    if message.author == bot.user:
        return

    # Log the message in console, change output to log file later.
    log(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have permission to use this command.')

# Implements the quoting functionality.
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
@bot.command(name='mirror', help='Repeats what you say')
async def mirror(ctx):
    message = ctx.message.content.split(' ', 1)[1]
    await ctx.message.channel.send(message)

# Reminder feature, like the one on Reddit.
@bot.command(name='remindme', help='Sets a reminder for you')
async def reminder(ctx):
    global reminders
    d = await set_reminder(ctx)
    reminders.append(d)
    print(reminders)
    reminders = sorted(reminders, key = lambda i : i['time'])
    print(reminders)

# Show all reminders.
@bot.command(name='reminders', help='Shows a list of reminders')
async def reminderList(ctx):
    global reminders
    reminderList = []
    for d in reminders:
        if d['id'] == ctx.message.author.id:
            reminderList.append(d)
    await showReminders(ctx, reminderList)

# Remove first reminder.
@bot.command(name='remove', help='Removes reminders')
async def remove(ctx):
    
    # Temporary variable to hold the first element.
    global reminders
    pop = None

    # Find the first reminder from the same user ID.
    for d in reminders:
        if d['id'] == ctx.message.author.id:
            pop = d
            break
    
    # Remove the element if not none.
    if pop is not None:
        reminders.remove(pop)
        await ctx.message.channel.send("Upcoming reminder removed.")
    else:
        await ctx.message.channel.send("There are no reminders to be removed.")

# uwutranslator, like the one on Reddit.
@bot.command(name='uwulate', help='Translate what you type into the language of the gods')
async def uwu(ctx):
    message = uwulate(ctx.message.content.split(' ', 1)[1])
    await ctx.message.channel.send(message)

# Dictionary for quick definition of words.
@bot.command(name='define', help='Searches your word in the dictionary')
async def define(ctx):
    await get_definition_normal(ctx)

# Dice roll for decisions if you want to leave it up to the gods.
@bot.command(name='roll', help='Rolls a random number between your choice')
async def roll(ctx):
    await roll_dice(ctx)

# Urban dictionary.
@bot.command(name='udict', help='Uses Urban Dictionary to find a word')
async def udict(ctx):
    await get_definition_urban(ctx)

# Log out and dump reminders into a file for persistency's sake.
@bot.command(name='nap', help='Shuts the bot down')
@commands.is_owner()
async def logout(ctx):

    # Good night...
    check_reminders.cancel()
    await ctx.message.channel.send("Good night...")

    # Convert the datetime object to a string first.
    for d in reminders:
        d['time'] = d['time'].strftime('%Y-%m-%d %H:%M:%S.%f')

    # Opens the json file for writing.
    with open('data/reminders.json', 'w+') as fp:
        json.dump(reminders, fp)
        fp.close()

    # Closes the bot gracefully.
    await bot.logout()

# Background task that checks reminders when the bot loads.
@tasks.loop(seconds=1.0)
async def check_reminders():

    # Alllow function to access the global variable.
    global reminders

    # Keep track of the removed entries.
    removed = []
    for d in reminders:
        if datetime.now() > d['time']:
            member = findMember(d['id'])
            if member is not None:
                await member.send(d['reminder'])
                removed.append(d)
    
    # Remove it after the loop.
    for d in removed:
        reminders.remove(d)

# Helper function to find a member.
def findMember(id):
    for g in bot.guilds:
        member = g.get_member(id)
        if member is not None:
            break
    return member
    
# ------------------ PERSISTENCE STARTS HERE ------------------ #
# Load json, but convert string to a datetime object.
with open('data/reminders.json', 'r') as fp:
    reminders = json.load(fp)
    for d in reminders:
        d['time'] = datetime.strptime(d['time'], '%Y-%m-%d %H:%M:%S.%f')
    fp.close()

# Run the bot, but try to catch RuntimeError from SIGINT (signal doesn't seem to work).
try:
    bot.run(env_token)

except RuntimeError:
    # Convert the datetime object to a string first.
    for d in reminders:
        d['time'] = d['time'].strftime('%Y-%m-%d %H:%M:%S.%f')

    # Opens the json file for writing.
    with open('data/reminders.json', 'w+') as fp:
        json.dump(reminders, fp)
        fp.close()
    print("Bot has been forcefully shut down.")
    
else:
    pass