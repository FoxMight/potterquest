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

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Ye old magic shop", description="", color=0xFFDF00)
        # get the entire pet list
        costs = ""
        items = ""
        i = 0

        for petObj in self.pets.values():
            items = items + petObj.name + "\n"
            costs = costs + str(petObj.cost) + " berries\n"
            i += 1

        embed.add_field(name="Pets: \n", value="Look at our magical pets for sale!", inline=False)
        embed.add_field(name="Name ", value=items, inline=True)
        embed.add_field(name="Cost ", value=costs, inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, type, name):
        type = type.lower()

        # if the type is a "pet" search for the name in the pet outline
        if str(type) == "pets":
            # see if the basic structure is available in the pet outline
            petObj = self.pets[name]
            if petObj is None:
                await ctx.send("That pet is not in the shop yet!")
                return

            # check how much money the user has

            userID = ctx.author.id

            # see if the user exists in the database
            userDoc = self.dbConnection.profileFind({"id": userID})
            if userDoc is None:
                await ctx.send("Please set up your profile first!")
                return

            userCoins = userDoc["coins"]

            if petObj.cost > userCoins:
                await ctx.send("You do not have enough money to buy that!")
                return
            userCoins = userCoins - petObj.cost
            # we already have a pet outline for the pet
            # and the userid, we just need to give the pet outline copy
            usersPet = copy.copy(petObj)
            updatePetDetails(self.dbConnection, userDoc, userID, usersPet)
            # save the pet
            savePet(self.dbConnection, usersPet)

            # letters in vowel as a list
            vowels = ["a", "e", "i", "o", "u"]
            if (petObj.type)[0].lower() in vowels:
                msg = "Buying an " + petObj.type + "!"
            else:
                msg = "Buying a " + petObj.type + "!"
            self.dbConnection.profileUpdate({"id": userID}, {"$set": {"coins": userCoins}})
        else:
            msg = "Please provide a valid set to buy from!"

        await ctx.send(msg)


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(shop(client, database_connection))
