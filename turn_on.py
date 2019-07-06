import discord
import sys
import signal
import os
import asyncio
import pymongo
import gridfs
import secret
from discord.ext import commands


# a signal handler to handle shutdown of the bot from the terminal
def signal_handler(sig, frame):
    print('Closing bot...')
    sys.exit(0)

TOKEN = secret.secret_token

# initializing discord client
client = commands.Bot(command_prefix='+')
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')


client.remove_command('help')
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="The general list of commands", color=0xFFFFFF)
    embed.add_field(name="Basic Commands", value="+help \n +start (generates a profile)\n +shop  ", inline=False)
    embed.add_field(name="Commands that require a profile",
                    value="+profile \n +coins \n +birthday \n +house \n+setpfp \n +nameUpdate", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

"""
    Old fun commands that need to be re-implemented
    if message.content.startswith('+cheese'):
        id = message.author.id
        if(id == '93121870949281792'):
            msg = "GIMME MY DAMN CHEESE"
            await client.send_message(message.channel, msg)

    if message.content.startswith('+ariana'):
        #will have to change
        id = message.author.id
        if(id == '110586016921862144'):
            with open ('D:\\OneDrive\\CS_Projects\\Potterquest\\image2.jpg', 'rb') as picture:
                 await client.send_file(message.channel, picture)

"""



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Quidditch'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

if __name__ == '__main__':
    # sets up signal to be recognized by user
    signal.signal(signal.SIGINT, signal_handler)
    #for every filaname in the cogs directory...
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            #load the cog
            client.load_extension(f'cogs.{filename[:-3]}')


    client.run(TOKEN)
