import discord, json
from datetime import datetime
from discord.ext import commands
from modules.utilities.logger import *

# System cog.
class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[{timestamp()}] Logged in as {self.bot.user}!')
        reminder_cog = self.bot.get_cog('Reminders')
        reminder_cog.check_reminders.start()

    @commands.Cog.listener()
    async def on_message(self, message):

        # Stops bot from trigger responses to its own messages.
        if message.author == self.bot.user:
            return

        # Log the message in console, change output to log file later.
        log(f'[{timestamp()}] Message from {message.author}: {message.content}')
        # await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have permission to use this command.')

    # Mirrors whatever the user says, sends it back to you as a PM.
    @commands.command(help='Repeats what you say')
    async def mirror(self, ctx):
        message = ctx.message.content.split(' ', 1)[1]
        await ctx.message.channel.send(message)

    # Log out and dump reminders into a file for persistency's sake.
    @commands.command(help='Shuts the bot down')
    @commands.is_owner()
    async def nap(self, ctx):

        # Good night...
        reminder_cog = self.bot.get_cog('Reminders')
        reminder_cog.check_reminders.cancel()
        reminders = reminder_cog.getRemindersList()
        await ctx.message.channel.send("Good night...")

        # Convert the datetime object to a string first.
        for d in reminders:
            d['time'] = d['time'].strftime('%Y-%m-%d %H:%M:%S.%f')

        # Opens the json file for writing.
        with open('data/reminders.json', 'w+') as fp:
            json.dump(reminders, fp)
            fp.close()

        # Closes the bot gracefully.
        await self.bot.logout()