from typing import Any

import discord
import sys
import signal
import os
import asyncio
import pymongo
import gridfs
from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionNotLoaded

import secret
from discord.ext import commands
from cogs.management import owner_admin_test
from database_connection import database_connection

# initializing the database
global_db_connection: database_connection = database_connection()


def prefix(bot, ctx):
    """
    :param bot: Our bot instance
    :param ctx: The context
    :return:
    """

    global global_db_connection

    id = ctx.guild.id
    server = global_db_connection.server_find({'id': id})

    if server is None:
        global_db_connection.server_insert({'id': id, 'prefix': 'fox '})
        server = global_db_connection.server_find({'id': id})

    p = server['prefix']
    return p


# a signal handler to handle shutdown of the bot from the terminal
def signal_handler(sig, frame):
    print('Closing bot...')
    sys.exit(0)


TOKEN = secret.secret_token

# initializing discord client
client = commands.Bot(command_prefix=prefix, case_insensitive=True)


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
    result = owner_admin_test(ctx, global_db_connection)

    if result is False:
        msg = "You do not have permission to load commands!"
        await ctx.send(msg)
        return
    else:
        msg = ""
        try:
            client.load_extension(f"cogs.{extension}")
            msg = "Extension loaded successfully."
        except ExtensionAlreadyLoaded:
            msg = "Extension has already been loaded."

        await ctx.send(msg)
        return


@client.command()
async def unload(ctx, extension):
    result: bool = owner_admin_test(ctx, global_db_connection)
    if result is False:
        msg = "You do not have permission to load commands!"
        await ctx.send(msg)
        return
    else:
        msg = ""
        try:
            client.unload_extension(f'cogs.{extension}')
            msg = "Extension unloaded successfully."
        except ExtensionNotLoaded:
            msg = "Extension has already been unloaded."

        await ctx.send(msg)
        return



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
    # for every filaname in the cogs directory...
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # load the cog
            client.load_extension(f'cogs.{filename[:-3]}')

    client.run(TOKEN)
