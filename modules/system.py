import discord, json
from datetime import datetime
from discord.ext import commands
from .utilities.logger import *

# System cog.
class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        # Activate background checks.
        print(f'[{timestamp()}] Logged in as {self.bot.user}!')
        reminder_cog = self.bot.get_cog('Reminders')
        reminder_cog.check_reminders.start()

        # Fluff.
        custom_activity = discord.Game(name="Discord")
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=custom_activity)

    @commands.Cog.listener()
    async def on_message(self, message):

        # Stops bot from trigger responses to its own messages.
        if message.author == self.bot.user:
            return

        # Log the message in console, change output to log file later.
        log(f'[{timestamp()}] Message from {message.author}: {message.content}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have permission to use this command.')

    # Mirrors whatever the user says, sends it back to you as a PM.
    @commands.command(help='Repeats what you say')
    async def mirror(self, ctx):
        message = ctx.message.content.split(' ', 1)[1]
        await ctx.message.channel.send(message)
        
    # Test command to check if bot is online.
    @commands.command(help='Test command to check if bot is online.')
    async def test(self, ctx):
        await ctx.message.channel.send("Hello world!")

    # Log out and dump reminders into a file for persistency's sake.
    # Handled by 'atexit' module.
    @commands.command(help='Shuts the bot down')
    @commands.is_owner()
    async def nap(self, ctx):

        # Alert everyone that bot is shutting down.
        await ctx.message.channel.send("Good night...")

        # Closes the bot gracefully.
        await self.bot.logout()