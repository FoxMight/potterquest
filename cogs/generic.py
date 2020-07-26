import discord
from discord.ext import commands


class Generic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx):
        # creates message and sends
        msg = 'Hello {0.author.mention}'.format(ctx)
        await ctx.send(msg)


def setup(client):
    client.add_cog(Generic(client))
