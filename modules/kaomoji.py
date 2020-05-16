import discord
import re
import json
import glob
from .utilities.logger import *
from discord.ext import tasks, commands
from datetime import datetime


class Kaomoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.kDict = self.initKaomojiCog()

    # Load kaomojis.
    def initKaomojiCog(self):

        # Gets all the available kaomojis.
        files = glob.glob("data/kaomoji/*.json")

        # Append each file into the list.
        kaomojis = []
        for fpath in files:
            with open(fpath, 'r') as fp:
                kaomojis.append(json.load(fp))
                fp.close()

        # Merge the files into one dictionary.
        kDict = dict()
        for k in kaomojis:
            kDict = {**kDict, **k}

        print(kDict)
        return kDict
    
    # Either gets you a list of kaomojis or gives you a list of categories for kaomojis.
    @commands.command(help='Lists kaomojis available')
    async def klist(self, ctx):

        await ctx.message.author.send("To be implemented.")
        await ctx.message.channel.send("A list of available kaomojis have been sent to your DMs.")
