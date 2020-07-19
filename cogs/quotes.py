import discord
from discord.ext import commands
from pets import pet, readPetOutline, savePet, updatePetDetails
from databaseConnection import databaseConnection
import copy


class quotes(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(quotes(client, database_connection))
