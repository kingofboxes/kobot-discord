import json
import discord
from discord.ext import tasks, commands
from googleapiclient.discovery import build

# Dice module.
class Search(commands.Cog):

    def __init__(self, bot, csj, cse):
        self.bot = bot
        self._csj = csj
        self._cse = cse

    # Searches Google using keys.
    @commands.command(help='Search Reddit via Google (because Reddit search sucks)')
    async def reddit(self, ctx):

        # Get the search term.
        search_term = ctx.message.content.split()

        # Scrape it using CSE.
        if len(search_term) > 1:
            query = ' '.join(search_term[1:]) + " reddit"
            service = build("customsearch", "v1", developerKey=self._csj)
            res = service.cse().list(q=query, cx=self._cse).execute()
            if 'items' in list(res.keys()): 
                await self.processRedditJson(ctx, res)
            else:
                await ctx.message.channel.send("Could not find any results.")

        else:
            await ctx.message.channel.send("```Usage: !reddit <phrase>```")

    async def processRedditJson(self, ctx, file):

        # Extract the items from the file.
        data = file['items']
        display = len(data)

        # Restrict the post to 5 links.
        if display > 5: display = 5

        # Process the item block.
        if data is not None or display == 0:
            message = ''
            index = 1
            for d in data:
                message = message + f"**[#{index}] {d['title']}**\n<{d['link']}>\n\n"
                index += 1
                if index > display: break
            await ctx.message.channel.send(message)

        else:
            await ctx.message.channel.send("Could not find any results.")

    
    
