import discord
from discord.ext import commands
from pets import Pet, read_pet_outline, save_pet, update_pet_details
from databaseConnection import databaseConnection
import copy


class memes(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(memes(client, database_connection))
