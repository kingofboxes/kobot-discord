import discord
from discord.ext import commands
from .utilities.logger import *

# Everyday, we stray further from God's light.
class Uwulate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Listens for the wheelchair emoji.
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # Representations of emojis.
        wheelchair_emoji = b'\xe2\x99\xbf'

        # Triggers the uwulating module.
        if(reaction.emoji.encode() == wheelchair_emoji):
            log(f'[{timestamp()}] {user.name} uwulated message: {reaction.message.content}')
            await self.uwulateMessage(reaction, user)
            await reaction.message.remove_reaction(reaction.emoji, user)

    # Quotes a message by creating an rich embed.
    async def uwulateMessage(self, reaction, user):
        embed = self.createEmbed(reaction, user)
        await reaction.message.channel.send(content=f"**{user.name}** uwulated a message by **{reaction.message.author.mention}**:", embed=embed)

    # Embeds the uwulated message.  
    def createEmbed(self, reaction, user):
        embed = discord.Embed(title=None, description=None, color=0x2e86c1)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Uwulated message:", value=f"{self.uwulateHelper(reaction.message.content)}", inline=False)
        return embed

    # Translates a string.
    def uwulateHelper(self, message):
        message = message.lower()
        message = message.replace('l', 'w')
        message = message.replace('r', 'w')
        message = message.replace("to", "tuwu")
        message = message.replace("no", "nyo")
        message = message.replace("mo", "myo")
        message = message.replace("na", "nya")
        message = message.replace("my", "mwy")
        message = message.replace("ni", "nyi")
        message = message.replace("nu", "nyu")
        message = message.replace("ne", "nye")
        message = message.replace("du", "dwu")
        message = message.replace("the", "da")
        message = message.replace("go", "gwo")
        message = message.replace("you", "yow")
        message = message.replace("anye", "ane")
        message = message.replace("inye", "ine")
        message = message.replace("onye", "one")
        message = message.replace("unye", "une")
        message = message.replace("thank", "dank")
        return message