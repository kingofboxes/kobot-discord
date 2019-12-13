import discord
from discord.ext import commands
from datetime import datetime, timedelta

def uwulate(message):
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

# Quotes a message by creating an rich embed.
async def uwulateMessage(reaction, user, bot):
    
    # Variables used in quoting.
    quote_quoter = user.name

    # Channel which the message was sent.
    channel = reaction.message.channel
    embed = createEmbwed(reaction, user, bot)
    await channel.send(content=f"**{quote_quoter}** uwulated a message by **{reaction.message.author.mention}**:", embed=embed)

# Creates the rich embed.
def createEmbwed(reaction, user, bot):
    
    message = reaction.message.content

    # Embeds the uwulated message.  
    embed = discord.Embed(title=None, description=None, color=0x2e86c1)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="Uwulated message:", value=f"{uwulate(message)}", inline=False)

    return embed