import discord
from discord.ext import commands

# For regular dictionary.
from wn import WordNet
from wn.info import WordNetInformationContent
from wn.constants import wordnet_30_dir, wordnet_33_dir

# For urban dictionary.
import urllib.request, json

# Everyday, we stray further from God's light.
class Dictionary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # WordNet dictionary.
    @commands.command(help='Searches your word in the dictionary')
    async def define(self, ctx):

        # Create instance of wordnet, get the query from context and find synsets via WordNet.
        wordnet = WordNet(wordnet_30_dir)
        query = ctx.message.content.split(' ', 1)[1]
        synset = wordnet.synsets(query)
        
        # String manipulation to get a list of definitions.
        definitions = ""
        index = 1

        # Formulates the definitions.
        if len(synset) > 0:
            for syn in synset:
                if(query in syn.name()):
                    definitions = definitions + f"{index}. [{self.categorise(syn.name())}] {syn.definition()}\n"
                    index += 1
            await ctx.message.channel.send(f"```\nDefinition of {query}:\n{definitions}```")
        else:
            await ctx.message.channel.send(f"Could not find requested word, doing a secondary search in Urban Dictionary...")
            await self.udictHelper(ctx)   
        
    # Categorises word based on the synset name.
    def categorise(self, word):
        if '.n.' in word:
            return "noun"
        elif '.a.' in word:
            return "adj"
        elif '.v.' in word:
            return "verb"
        elif '.r.' in word:
            return "adv"
        else:
            return "n/a"

    # Urban Dictionary.
    # Gets the definition of the word from Urban Dictionary.
    @commands.command(help='Uses Urban Dictionary to find a word')
    async def udict(self, ctx):
        await udictHelper(ctx)
          
    # Actual function which does everything.
    async def udictHelper(self, ctx):

        # Sets up variables to use for webscraping.
        query = ctx.message.content.split(' ', 1)[1]
        parseQuery = query.replace(' ', '+')
        url = "http://api.urbandictionary.com/v0/define?term=" + parseQuery
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        # If not empty...
        if len(data) > 0:

            # Sort the data based on thumbs up.
            definitions = sorted(data['list'], key = lambda i : i['thumbs_up'], reverse=True)[0:3]
            block = ""
            index = 1

            # Organise into the right format.
            for d in definitions:
                definition = self.strip_artefacts(d['definition'])
                if d['example'][-2:] != '\n':
                    block = block + f"{index}. {definition} ({d['thumbs_up']} thumbs up)\n\n{self.strip_artefacts(d['example'])}\n\n"
                else:
                    block = block + f"{index}. {definition} ({d['thumbs_up']} thumbs up)\n\n{self.strip_artefacts(d['example'])}\n"
                index += 1

            message = f"Searching Urban Dictionary for {query}...\n```{block}```"

        else:
            message = f"Could not find requested word on Urban Dictionary."   
            
        await ctx.message.channel.send(message)
        
    # Strips the string.
    def strip_artefacts(self, string):

        # Strip the brackets.
        string = string.replace('[', '')
        string = string.replace(']', '')
        
        # In case of doubles...
        string = string.replace('\r\n\r\n', '\r\n')
        return string
