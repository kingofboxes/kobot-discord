import discord
from datetime import datetime, timedelta
from discord.ext import tasks, commands

# Sets the reminder and returns a dictionary.
async def set_reminder(ctx):

    message = ctx.message.content
    member = ctx.message.author

    # Maximum amount of times the string should be split is 2.
    input = message.split(' ', 2)

    # If there's only 1 thing in the list, it'll be a default implementation.
    # Default reminder: 10 minutes.
    duration = "10"

    if len(input) == 1:
        reminder = f"Reminding you for something you've set {duration} minutes ago."
    elif len(input) == 2:
        if input[1].lstrip("-").isdigit():
            duration = input[1]
            if int(duration) <= 0:
                await handleReminderCases(ctx, True)
                return
            reminder = f"Reminding you for something you've set {input[1]} minutes ago."
        else:
            reminder = f"Reminding you for something you've set 10 minutes ago: {input[1]}."
    else:
        if input[1].isdigit():
            duration = input[1]
            reminder = f"Reminder from {input[1]} minutes ago: {input[2]}."
        else:
            await handleReminderCases(ctx)
            return

    d_reminder = {'id' : member.id,
                'reminder' : reminder,
                'time' : datetime.now() + timedelta(minutes=int(duration))}

    confirmation = f"Reminder set. Reminding you in {duration} minutes."
    await ctx.message.channel.send(confirmation)
    return d_reminder

# Handles edge cases.
async def handleReminderCases(ctx, integer=False):
    if integer is False:
        usage_message = "```Usage: !remindme [time] [description]```"
    else:
        usage_message = "Please enter a non-negative or non-zero integer for time."

    await ctx.message.channel.send(usage_message)

# Show reminders.
async def showReminders(ctx, reminders):

    if len(reminders) == 0:
        await ctx.message.author.send("You do not have any reminders.")
        return
    else:
        index = 1
        message = "Your list of reminders:\n"
        for d in reminders:
            message = message + f"[{index}] {d['time'].strftime('%Y-%m-%d %H:%M:%S')}: {d['reminder']}\n"
            index += 1
    
    message = f"```\n{message}\n```"
    await ctx.message.author.send(message)



