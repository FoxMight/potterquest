from discord.ext import commands
from databaseConnection import databaseConnection


class memes(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(memes(client, database_connection))
