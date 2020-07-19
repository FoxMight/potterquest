import discord
from discord.ext import commands
from pets import pet, readPetOutline, savePet, updatePetDetails
from databaseConnection import databaseConnection
import copy


class shop(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection
        self.pets = readPetOutline(databaseConnection)
        # Debugging code to check what pets got loaded in:
        # for petObj in self.pets.values():
        #     print(petObj.type)



def setup(client):
    database_connection = databaseConnection()
    client.add_cog(shop(client, database_connection))
