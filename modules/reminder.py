import discord
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from .reminderHelper import *

remindersList = []

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
        elif input[2].isdigit():
            duration = input[2]
            reminder = "Reminder from " + input[2] + " minutes ago: \"" + input[1] + "\"." 
        else:
            await member.create_dm()
            await member.dm_channel.send("Please specify the duration (in minutes) of when you would like to be reminded.")
            return

    remindersList.append(reminderHelper(member, duration, reminder, remindersList))
