import discord
from discord.ext import commands
from .utilities.logger import *
from datetime import datetime, timedelta
import pytz

# Quote module.
class Quote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Listens for reactions added to comments.
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # Encoded value of asterisk emoji.
        asterisk_emoji = b'*\xef\xb8\x8f\xe2\x83\xa3'

        # Triggers the quote module if asterisk.
        if(reaction.emoji.encode() == asterisk_emoji):
            log(f'[{timestamp()}] {user.name} quoted message: {reaction.message.content}')
            await self.quoteMessage(reaction, user)
            await reaction.message.remove_reaction(reaction.emoji, user)

    # Quotes a message by creating an rich embed.
    async def quoteMessage(self, reaction, user):
    
        # Create an embed to send.
        embed = self.createEmbed(reaction, user)

        # Channel which the message was sent.
        channel = reaction.message.channel
        await channel.send(content = f"**{user.name}** quoted **{reaction.message.author.mention}**:", embed=embed)

    # Creates the rich embed.
    def createEmbed(self, reaction, user):
        
        # Timezone difference, Discord uses UTC.
        tz = pytz.timezone('Australia/Sydney')
        time_sent = pytz.utc.localize(reaction.message.created_at, is_dst=None).astimezone(tz)

        # Retrieve the urls for the attachment of the quoted message.
        url = None
        for a in reaction.message.attachments:
            if '.png' in a.url or '.jpg' in a.url:
                url = a.url

        embed = discord.Embed(title=None, description=None, color=0x2e86c1)
        embed.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)

        # If the message is just an image upload, don't add a field.
        if reaction.message.content != '':
            embed.add_field(name="Original message:", value=f"{reaction.message.content}", inline=False)

        # If there is a URL, add an attachments field and a direct link to it.
        if url is not None:
            embed.add_field(name="Attachments:", value=url, inline=False)
            embed.set_image(url=url)

        embed.set_footer(text="Date sent: {0}".format(time_sent.strftime("%d/%m/%Y, %H:%M")))
        return embed
        