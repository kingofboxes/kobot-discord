# External modules.
import os, discord, json
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks

# Import the cogs.
from system import System
from modules.utilities.logger import *
from modules.dice import Dice
from modules.quote import Quote
from modules.uwulate import Uwulate
from modules.dictionary import Dictionary
from modules.reminder import Reminders
from modules.search import Search

# Load the required variables from .env file.
load_dotenv()
env_token = os.getenv('DISCORD_TOKEN')
csj_token = os.getenv('CSJ_TOKEN')
cse_token = os.getenv('CSE_TOKEN')

# Instantiate a client and run it.
bot = commands.Bot(command_prefix='!')

# Loads the reminders.
with open('data/reminders.json', 'r') as fp:
    reminders = json.load(fp)
    for d in reminders:
        d['time'] = datetime.strptime(d['time'], '%Y-%m-%d %H:%M:%S.%f')
    fp.close()

# Add cogs to the bot.
bot.add_cog(System(bot))
bot.add_cog(Dice(bot))
bot.add_cog(Quote(bot))
bot.add_cog(Uwulate(bot))
bot.add_cog(Dictionary(bot))
bot.add_cog(Reminders(bot, reminders))
bot.add_cog(Search(bot, csj_token, cse_token))

# Hold onto reminders cog.
reminder_cog = bot.get_cog('Reminders')

# Run the bot, but try to catch RuntimeError from SIGINT (signal doesn't seem to work).
try:
    bot.run(env_token)
    
except RuntimeError:

    # Cancel the background task and get the list of reminders.
    reminder_cog.check_reminders.cancel()
    reminders = reminder_cog.getRemindersList()

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