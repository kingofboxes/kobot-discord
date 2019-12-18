import discord
import re
from .utilities.logger import *
from discord.ext import tasks, commands
from datetime import datetime
from dateutil.relativedelta import *

# Dice module.
class Reminders(commands.Cog):

    def __init__(self, bot, reminders):
        self.bot = bot
        self._reminders = reminders

    # Sets the reminder and returns a dictionary.
    @commands.command(help='Sets a reminder for you')
    async def remindme(self, ctx):

        # Use cases:
        # !remindme <duration>
        # !remindme <duration> <message>
        input = ctx.message.content.split(' ', 2)
        summary = "(no description)"
        curr_time = datetime.now()
        curr_time_s = curr_time.strftime("%d/%m/%Y at %H:%M:%S")
        valid = False

        # Put together the reminder.
        if len(input) == 1:
            pass

        elif len(input) == 2:
            duration = self.generateDuration(input[1])
            if duration is not None:
                valid = True

        else:
            duration = self.generateDuration(input[1])
            if duration is not None:
                valid = True
                summary = input[2]

        # Send the reminder or usage information.
        if valid:
            
            # Create a dictionary.
            d_reminder = {  'id' : ctx.message.author.id,
                            'reminder' : f"Your reminder from {curr_time_s}: {summary}",
                            'summary' : summary,
                            'time' : curr_time + relativedelta(years=+duration[0], months=+duration[1], days=+duration[2], hours=+duration[3], minutes=+duration[4])}

            # Append the dictionary to the list of reminders and sorts it.
            reminder_time = d_reminder['time'].strftime("%d/%m/%Y at %H:%M:%S")
            message = f"Reminder set for {reminder_time}."
            self._reminders.append(d_reminder)
            
        else:
            message = "```Usage: !remindme <time> [description]\ntime = #Y#M#d#h#m (e.g. 1Y1d1h1m = 1 year, 0 months, 1 day, 1 hour, 1 minute)```"

        await ctx.message.channel.send(message)
             
    # Background task that checks reminders when the bot loads.
    @tasks.loop(seconds=1.0)
    async def check_reminders(self):
        
        # Sort the reminders everytime you check.
        # print(self._reminders)
        self._reminders = sorted(self._reminders, key = lambda i : i['time'])

        # Keep track of the removed entries.
        removed = []
        for d in self._reminders:
            if datetime.now() > d['time']:
                member = self.findMember(d['id'])
                if member is not None:
                    await member.send(d['reminder'])
                    removed.append(d)
        
        # Remove it after the loop.
        for d in removed:
            self._reminders.remove(d)

    # Helper function to find a member.
    def findMember(self, id):
        for g in self.bot.guilds:
            member = g.get_member(id)
            if member is not None:
                break
        return member

    # Getter for reminders list.
    def getRemindersList(self):
        return self._reminders

    # Uses regex to get the fields to make a new relativedelta object.
    # Group 1 = Year, Group 2 = Month, 
    # Group 3 = Day, Group 4 = Hour, 
    # Group 5 = Minute
    def generateDuration(self, dateStr):
        
        # Constants
        MINUTES_IN_YEAR = 525600
        MINUTES_IN_MONTH = 43800
        MINUTES_IN_DAY = 1440
        MINUTES_IN_HOUR = 60

        dateFmt = r"^\s*(?:(\d+)Y)?" + \
                r"\s*(?:(\d+)M)?" + \
                r"\s*(?:(\d+)d)?" + \
                r"\s*(?:(\d+)h)?" + \
                r"\s*(?:(\d+)m)?\s*$"

        match = re.search(dateFmt, dateStr)
        if match is not None:
            duration = [int(x) for x in match.groups(default="0")]
            return duration

    # Returns a list of reminders.
    @commands.command(help='Gives you a list of your reminders')
    async def reminders(self, ctx):

        # Get a list of your own reminders.
        pReminders = self.getPersonalReminders(ctx)

        # Show reminders.
        if len(pReminders) == 0:
            await ctx.message.channel.send("You do not have any reminders.")
            return
        else:
            index = 1
            message = "Your list of reminders:\n"
            for d in pReminders:
                message = message + f"[{index}] {d['time'].strftime('%Y-%m-%d %H:%M:%S')}: {d['summary']}\n"
                index += 1
        
        message = f"```\n{message}\n```"
        await ctx.message.channel.send(message)

    # Helper to get list of your own reminders.
    def getPersonalReminders(self, ctx):
        pReminders = []
        for d in self._reminders:
            if d['id'] == ctx.message.author.id:
                pReminders.append(d)
        return pReminders