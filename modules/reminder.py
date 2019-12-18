import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta

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
        summary = "No reminder description specified."
        valid = False

        # Put together the reminder.
        if len(input) == 1:
            pass

        elif len(input) == 2:
            if input[1].lstrip("-").isdigit():
                duration = input[1]
                if int(duration) > 0: valid = True
                reminder = f"Reminding you for something you've set {input[1]} minutes ago."

        else:
            if input[1].lstrip("-").isdigit():
                duration = input[1]
                summary = input[2]
                if int(duration) > 0: valid = True
                reminder = f"Reminder from {input[1]} minutes ago: {input[2]}."

        # Send the reminder or usage information.
        if valid:
            
            # Create a dictionary.
            d_reminder = {'id' : ctx.message.author.id,
                    'reminder' : reminder,
                    'summary' : summary,
                    'time' : datetime.now() + timedelta(seconds=int(duration))}

            # Append the dictionary to the list of reminders and sorts it.
            message = f"Reminder set. Reminding you in {duration} minutes."
            self._reminders.append(d_reminder)
            
        else:
            message = "```Usage: !remindme <time> [description]; time >= 0```"

        await ctx.message.channel.send(message)
             
    # Background task that checks reminders when the bot loads.
    @tasks.loop(seconds=1.0)
    async def check_reminders(self):
        
        # Sort the reminders everytime you check.
        print(self._reminders)
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
