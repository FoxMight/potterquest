import discord
from discord.ext import commands
from database_connection import database_connection


class Server(commands.Cog):

    def __init__(self, client, inner_database_connection):
        self.client = client
        self.database_connection = inner_database_connection

    @commands.command()
    async def serverinfo(self, ctx):
        return

    @commands.command()
    async def prefix(self, ctx, *, p=None):
        id = ctx.guild.id
        server = self.database_connection.server_find({'id': id})

        # if trying to change prefix
        if p is not None:
            # if is server admin
            if ctx.guild.get_member(ctx.author.id).guild_permissions.administrator:
                if server is None:
                    self.database_connection.server_insert({'id': id, 'prefix': p})
                else:
                    self.database_connection.server_update({'id': id}, {'$set': {'prefix': p}})

                embed = discord.Embed(
                    color=discord.Color.gold(),
                    title='Prefix Change',
                    description='Server prefix set to `' + p + '`.'
                )

                await ctx.send(embed=embed)
            # not admin but trying to change prefix
            else:
                embed = discord.Embed(
                    color=discord.Color.gold(),
                    title='Prefix Change',
                    description='Sorry, you have to be a server admin to do that!'
                )

                await ctx.send(embed=embed)
        # prompt & say prefix
        else:
            if server is None:
                self.database_connection.server_insert({'id': id, 'prefix': '+'})
                server = self.database_connection.server_find({'id': id})

            p = server['prefix']

            embed = discord.Embed(
                color=discord.Color.gold(),
                title='Prefix',
                description='Server prefix is `' + p + '`.\nTo change your server prefix, use `+prefix <prefix>`.'
            )

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Server(client, database_connection()))
    return
