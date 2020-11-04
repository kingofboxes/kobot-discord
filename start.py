# External modules.
import os, discord, json, atexit
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks

# Import the cogs.
from modules.utilities.logger import *
from modules.system import System
from modules.dice import Dice
from modules.quote import Quote
from modules.uwulate import Uwulate
from modules.dictionary import Dictionary
from modules.reminder import Reminders
from modules.kaomoji import Kaomoji

# Cleans up when program exits.
def cleanup():

    # Cancel the background task and get the list of reminders.
    reminder_cog.check_reminders.cancel()
    reminders = reminder_cog.getRemindersList()

    # Convert the datetime object to a string first.
    for d in reminders:
        d['time'] = d['time'].strftime('%Y-%m-%d %H:%M:%S.%f')

    # Opens the json file for writing.
    with open('data/reminders.json', 'w+') as fp:
        json.dump(reminders, fp, indent=3)
        fp.close()

    print("Bot has been shut down.")

# Load the required variables from .env file.
load_dotenv()
env_token = os.getenv('DISCORD_TOKEN')

# Intents update for Discord.py 1.5.1.
intents = discord.Intents.default()
intents.members = True

# Instantiate a client and run it.
bot = commands.Bot(command_prefix='.', intents=intents)

# Loads the reminders.
if os.path.exists('data/reminders.json'):
    with open('data/reminders.json', 'r') as fp:
        reminders = json.load(fp)
        for d in reminders:
            d['time'] = datetime.strptime(d['time'], '%Y-%m-%d %H:%M:%S.%f')
        fp.close()
else:
    reminders = []

# Add cogs to the bot.
bot.add_cog(System(bot))
bot.add_cog(Dictionary(bot))
bot.add_cog(Reminders(bot, reminders))

# Disabled cogs to save memory.
# bot.add_cog(Dice(bot))
# bot.add_cog(Quote(bot))
# bot.add_cog(Uwulate(bot))
# bot.add_cog(Kaomoji(bot))

# Hold onto reminders cog.
reminder_cog = bot.get_cog('Reminders')

# Run the bot, but try to catch RuntimeError from SIGINT (signal doesn't seem to work).
atexit.register(cleanup)
bot.run(env_token)
