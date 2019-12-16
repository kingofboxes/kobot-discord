# For regular dictionary.
from wn import WordNet
from wn.info import WordNetInformationContent
from wn.constants import wordnet_30_dir, wordnet_33_dir

# For urban dictionary.
import urllib.request
import json

# WordNet dictionary.
# Gets the definition of the word.
async def get_definition_normal(ctx):

    # Create instance of wordnet.
    wordnet = WordNet(wordnet_30_dir)

    # Get the query from context and find synsets via WordNet.
    query = ctx.message.content.split(' ', 1)[1]
    synset = wordnet.synsets(query)
    
    # String manipulation to get a list of definitions.
    definitions = ""
    index = 1

    if len(synset) > 0:
        for syn in synset:
            if(query in syn.name()):
                definitions = definitions + f"{index}. [{categorise(syn.name())}] {syn.definition()}\n"
                index += 1
        await ctx.message.channel.send(f"```\nDefinition of {query}:\n{definitions}```")
    else:
        await ctx.message.channel.send(f"Could not find requested word in dictionary, doing a secondary search in Urban Dictionary...")
        await get_definition_urban(ctx)   

    
# Categorises word based on the synset name.
def categorise(word):
    
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
async def get_definition_urban(ctx):

    query = ctx.message.content.split(' ', 1)[1]
    parseQuery = query.replace(' ', '+')
    url = "http://api.urbandictionary.com/v0/define?term=" + parseQuery
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    if not data:

        definitions = sorted(data['list'], key = lambda i : i['thumbs_up'], reverse=True)[0:3]
        
        block = ""
        index = 1

        for d in definitions:
            definition = strip_artefacts(d['definition'])
            if d['example'][-2:] != '\n':
                block = block + f"{index}. {definition} ({d['thumbs_up']} thumbs up)\n\n{strip_artefacts(d['example'])}\n\n"
            else:
                block = block + f"{index}. {definition} ({d['thumbs_up']} thumbs up)\n\n{strip_artefacts(d['example'])}\n"
            index += 1

        message = f"Searching Urban Dictionary for {query}...\n```{block}```"

    else:
        message = f"Could not find requested word on Urban Dictionary."   
        
    await ctx.message.channel.send(message)

# Strips the string.
def strip_artefacts(string):

    # Strip the brackets.
    string = string.replace('[', '')
    string = string.replace(']', '')
    
    # In case of doubles...
    string = string.replace('\r\n\r\n', '\r\n')

    return string
