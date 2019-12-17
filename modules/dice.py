import discord
from discord.ext import commands
import random

# Dice module.
class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # All bets are off.
    @commands.command(help='Rolls a random number between your choice')
    async def roll(self, ctx):

        # Split the message in arguments.
        message = ctx.message.content
        input = message.split(' ', 2)

        # Default boundaries.
        lowerBound = 0
        upperBound = 1
        valid = True

        # Handles the cases.
        if len(input) == 1:
            pass
        elif len(input) == 2:
            if input[1].lstrip("-").isdigit():
                if int(input[1]) < 0: valid = False
                upperBound = int(input[1])
            else:
                valid = False
        else:
            if input[1].lstrip("-").isdigit() and input[2].lstrip("-").isdigit():
                if int(input[1]) > int(input[2]) or int(input[1]) < 0 or int(input[2]) < 0: valid = False
                lowerBound = int(input[1])
                upperBound = int(input[2])
            else:
                valid = False

        if valid:
            await ctx.message.channel.send(f"You rolled {random.randint(lowerBound, upperBound)} from a pool of numbers between {lowerBound} and {upperBound}.")
        else:
            await ctx.message.channel.send("```Usage: !roll [x] [y] (where x <= y; x, y >= 0)```") 





    