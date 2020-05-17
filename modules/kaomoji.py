import discord
import json
import glob
from discord.ext import tasks, commands

class Kaomoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._kDict = self.initKaomojiCog()

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

        return kDict

    # Getter for the dictionary.
    def getKDict(self):
        return self._kDict
    
    # Either gets you a list of kaomojis or gives you a list of categories for kaomojis.
    @commands.command(help='Lists kaomojis available')
    async def klist(self, ctx):

        # Use cases:
        # !klist
        # !klist <category>
        input = ctx.message.content.split(' ', 2)
        kDict = self.getKDict()
        categories = list(kDict.keys())

        # Only when klist itself is invoked.
        if len(input) == 1 or len(input) > 2:
            message = f"```Usage: !klist [category] (e.g. !klist joy)\nCurrent available categories are: {categories}```"
        
        # If only two arguments are specified.
        else:
            cat_arg = input[1]
            if cat_arg in categories:
                kaomoji = kDict[cat_arg]
                category = cat_arg.title()
                message = f"```{category}:\n"
                for k in kaomoji:
                    message = message + f"*\t{k}" + "\n"
                message = message + "```"

            else:
                message = f"Invalid category, please try again."

        # Check if message was sent in server or DM.
        if ctx.guild is not None:
            await ctx.message.channel.send("A list of available kaomojis have been sent to your DMs.")
        
        # Send the correct response to the person's DM.
        await ctx.message.author.send(message)