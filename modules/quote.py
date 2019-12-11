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

    embed = discord.Embed(title=None, description=None, color=0x00ff00)
    embed.set_author(name=quote_sender, icon_url=reaction.message.author.avatar_url)
    embed.add_field(name="Original message:", value=f"{quote_message}", inline=False)
    embed.add_field(name="Time sent:", value="{0}".format(time_sent.strftime("%d/%m/%Y, %H:%M:%S")), inline=False)
    
    return embed
    