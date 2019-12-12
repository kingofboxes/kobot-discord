import discord
from datetime import datetime, timedelta
from discord.ext import tasks, commands

# List of reminders.
remindersList = []

# Helper class for reminders.
class reminderHelper():
    def __init__(self, member, duration, reminder, remindersList):
        self.__member = member
        self.__reminder = reminder
        self.__remindersList = remindersList
        self.__reminderDue = datetime.now() + timedelta(minutes=int(duration))
        self.sendReminder.start()

    def stopReminderCheck(self):
        self.sendReminder.cancel()
        self.__remindersList.remove(self)

    @tasks.loop(minutes=1.0)
    async def sendReminder(self):
        if datetime.now() > self.__reminderDue:
            await self.__member.create_dm()
            await self.__member.dm_channel.send(self.__reminder)
            self.stopReminderCheck()

async def set_reminder(ctx):

    message = ctx.message.content
    member = ctx.message.author

    # Maximum amount of times the string should be split is 2.
    input = message.split(' ', 2)

    # Use cases: 
    #   - !remindme
    #   - !remindme <time>
    #   - !remindme <description>
    #   - !remindme <time> <description>
    #   - !remindme <description> <time>
    #   - !remindme <str> <str>

    # If there's only 1 thing in the list, it'll be a default implementation.
    # Default reminder: 10 minutes.
    duration = "10"

    if len(input) == 1:
        reminder = "Reminding you for something you've set " + duration + " minutes ago."
    elif len(input) == 2:
        if input[1].isdigit():
            duration = input[1]
            reminder = "Reminding you for something you've set " + input[1] + " minutes ago."
        else:
            reminder = "Reminding you for something you've set 10 minutes ago: \"" + input[1] + "\"."
    else:
        if input[1].isdigit():
            duration = input[1]
            reminder = "Reminder from " + input[1] + " minutes ago: \"" + input[2] + "\"."
        else:
            usage_message = "```Usage: !remindme [time] [description]```"
            await member.create_dm()
            await member.dm_channel.send(usage_message)
            return

    confirmation = "Reminder set. Reminding you in " + duration + " minutes."
    await ctx.message.channel.send(confirmation)

    remindersList.append(reminderHelper(member, duration, reminder, remindersList))
