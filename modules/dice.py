import discord, random

# All bets are off.
async def roll_dice(ctx):

    # Split the message in arguments.
    message = ctx.message.content
    input = message.split(' ', 2)

    # Default boundaries.
    lowerBound = 0
    upperBound = 1

    # Handles the cases.
    if len(input) == 1:
        pass
    elif len(input) == 2:
        if input[1].lstrip("-").isdigit():
            if int(input[1]) < 0:
                await handleDiceCases(ctx)
                return
            upperBound = int(input[1])
        else:
            await handleDiceCases(ctx)
            return
    else:
        if input[1].lstrip("-").isdigit() and input[2].lstrip("-").isdigit():
            if int(input[1]) > int(input[2]) or int(input[1]) < 0 or int(input[2]) < 0:
                await handleDiceCases(ctx)
                return
            lowerBound = int(input[1])
            upperBound = int(input[2])
        else:
            await handleDiceCases(ctx)
            return

    await ctx.message.channel.send(f"You rolled {random.randint(lowerBound, upperBound)} from a pool of numbers between {lowerBound} and {upperBound}.")

async def handleDiceCases(ctx):
    await ctx.message.channel.send("```Usage: !roll [x] [y] (where x <= y; x, y >= 0)```")

    