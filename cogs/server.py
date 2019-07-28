import discord
from discord.ext import commands
from databaseConnection import databaseConnection

class Server(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection

    @commands.command()
    async def serverinfo(self, ctx):
        return

    @commands.command()
    async def prefix(self, ctx, *, p = None):
        id = ctx.guild.id
        dbConnection = self.dbConnection
        server = dbConnection.serverFind({'id': id})

        #if trying to change prefix
        if (p is not None):
            #if is server admin
            if (ctx.guild.get_member(ctx.author.id).guild_permissions.administrator):
                if server is None:
                    dbConnection.serverInsert({'id': id, 'prefix': p})
                else:
                    dbConnection.serverUpdate({'id': id}, {'$set': {'prefix': p}})

                embed = discord.Embed(
                    color = discord.Color.gold(),
                    title = 'Prefix Change',
                    description = 'Server prefix set to `' + p + '`.'
                )

                await ctx.send(embed = embed)
            #not admin but trying to change prefix
            else:
                embed = discord.Embed(
                    color = discord.Color.gold(),
                    title = 'Prefix Change',
                    description = 'Sorry, you have to be a server admin to do that!'
                )

                await ctx.send(embed = embed)
        #prompt & say prefix
        else:
            if server is None:
                dbConnection.serverInsert({'id': id, 'prefix': '+'})
                server = dbConnection.serverFind({'id': id})

            p = server['prefix']

            embed = discord.Embed(
                color = discord.Color.gold(),
                title = 'Prefix',
                description = 'Server prefix is `' + p + '`.\nTo change your server prefix, use `+prefix <prefix>`.'
            )

            await ctx.send(embed = embed)

def setup(client):
    database_connection = databaseConnection()
    client.add_cog(Server(client, database_connection))
    return
