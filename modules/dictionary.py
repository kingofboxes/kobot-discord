import nltk
from nltk.corpus import wordnet as wn

nltk.download()

async def get_definition(ctx):

    syns1 = wn.synsets(ctx.message.content.split(' ', 1)[1])
    for syn in syns1:
        await ctx.message.channel.send(syn.definition())

    