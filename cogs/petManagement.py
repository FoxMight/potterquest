from databaseConnection import databaseConnection
from pets import pet, readUserPet
import discord
from discord.ext import commands


class petCommands(commands.Cog):
    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection

    @commands.command()
    async def pet(self, ctx):
        # show the user their pet!
        id = ctx.author.id
        name = ctx.author.name
        userDoc = self.dbConnection.profileFind({"id": id})
        if userDoc is None:
            await ctx.send("Please set up your profile first!")
            return

        # get the users petID
        petID = userDoc["currentPet"]

        # now read the pet in
        userPet = readUserPet(self.dbConnection, id, petID)
        userName = str(userDoc["username"])
        if userName.endswith("s"):
            titleOfPet = userName + "' " + "pet"
        else:
            titleOfPet = userName + "'s " + "pet"

        # now that we have the pet, create an embed for it!
        embed = discord.Embed(title=titleOfPet, description="", color=0xffffff)
        embed.add_field(name="Nickname", value=userPet.name, inline=False)
        embed.set_image(url=userPet.picture)

        await ctx.send(embed=embed)

    @commands.command()
    async def myPets(self, ctx):

        id = ctx.author.id

        # tell the user all their pet names, along with their corresponding ids
        userDoc = self.dbConnection.profileFind({"id": id})
        if userDoc is None:
            await ctx.send("Please set up your profile first!")
            return

        userName = str(userDoc["username"])
        if userName.endswith("s"):
            titleOfPets = userName + "' " + "pets"
        else:
            titleOfPets = userName + "'s " + "pets"

        embed = discord.Embed(title=titleOfPets, description="", color=0xffffff)
        # parse through all of the users pets

        # get their name, types and ids

        arrayOfPetIDs = userDoc["pets"]
        idList = ""
        typeList = ""
        nameList = ""

        for petID in arrayOfPetIDs:
            idList = idList + str(petID) + "\n"

            # create the corresponding pet object for this id
            userPet = readUserPet(self.dbConnection, id, petID)

            # now list its name, along with its type
            typeList = typeList + str(userPet.type) + "\n"
            nameList = nameList + str(userPet.name) + "\n"

        # now add it to the embed

        embed.add_field(name="Name ", value=nameList, inline=True)
        embed.add_field(name="Type ", value=typeList, inline=True)
        embed.add_field(name="ID ", value=idList, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def choosePet(self, ctx, idToSwitch):
        id = ctx.author.id
        try:
            num = int(idToSwitch)
        except ValueError:
            msg = "Please provide a valid pet ID."
            await ctx.send(msg)
            return

        # first see if they have that pet id
        userDoc = self.dbConnection.profileFind({"id": id})
        if userDoc is None:
            await ctx.send("Please set up your profile first!")
            return
        arrayOfPetIDs = userDoc["pets"]

        if not (num in arrayOfPetIDs):
            await ctx.send("Please provide a valid pet ID.")
            return

        petObj = readUserPet(self.dbConnection, id, int(idToSwitch))
        # now try to switch their current petID
        self.dbConnection.profileUpdate({"id": id}, {"$set": {"currentPet": int(idToSwitch), "pet": petObj.name}})
        await ctx.send("Pet set!")


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(petCommands(client, database_connection))
