import discord
from discord.ext import commands
from datetime import datetime, timedelta

# Quotes a message by creating an rich embed.
async def quoteMessage(reaction, user):
    
    # Variables used in quoting.
    quote_quoter = user.name
    quote_sender = reaction.message.author.name

    # Create an embed to send.
    embed = createEmbed(reaction, user)

    # Channel which the message was sent.
    channel = reaction.message.channel
    await channel.send(content = f"**{quote_quoter}** has quoted **{quote_sender}**:", embed=embed)

# Creates the rich embed.
def createEmbed(reaction, user):

    quote_sender = reaction.message.author.name
    quote_message = reaction.message.content
    time_sent = reaction.message.created_at + timedelta(hours=11)

    url = None
    attachments = reaction.message.attachments
    if attachments is not None:
        for a in attachments:
            if '.png' in a.url or '.jpg' in a.url:
                url = a.url

    embed = discord.Embed(title=None, description=None, color=0x00ff00)
    embed.set_author(name=quote_sender, icon_url=reaction.message.author.avatar_url)

    if quote_message != '':
        embed.add_field(name="Original message:", value=f"{quote_message}", inline=False)

    if url is not None:
        embed.add_field(name="Attachments:", value=url, inline=False)
        embed.set_image(url=url)

    embed.set_footer(text="Date sent: {0}".format(time_sent.strftime("%d/%m/%Y, %H:%M:%S")))

    return embed
    