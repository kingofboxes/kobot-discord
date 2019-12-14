from wn import WordNet
from wn.info import WordNetInformationContent
from wn.constants import wordnet_30_dir, wordnet_33_dir

# Gets the definition of the word.
async def get_definition(ctx):

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
        message = f"```\nDefinition of {query}:\n{definitions}```"  
    else:
        message = f"Could not find requested word in dictionary."   

    await ctx.message.channel.send(message)

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