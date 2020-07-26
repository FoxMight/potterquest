from database_connection import database_connection
from pets import Pet, read_user_pet
import discord
from discord.ext import commands


class pet_commands(commands.Cog):
    def __init__(self, client, inner_database_connection):
        self.client = client
        self.db_connection = inner_database_connection

    @commands.command()
    async def pet(self, ctx):
        # show the user their pet!
        id = ctx.author.id
        name = ctx.author.name
        userDoc = self.db_connection.profile_find({"id": id})
        if userDoc is None:
            await ctx.send("Please set up your profile first!")
            return

        # get the users petID
        petID = userDoc["currentPet"]

        # now read the pet in
        userPet = read_user_pet(self.db_connection, id, petID)
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
    async def my_pets(self, ctx):

        id = ctx.author.id

        # tell the user all their pet names, along with their corresponding ids
        user_doc = self.db_connection.profile_find({"id": id})
        if user_doc is None:
            await ctx.send("Please set up your profile first!")
            return

        user_name = str(user_doc["username"])
        if user_name.endswith("s"):
            titleOfPets = user_name + "' " + "pets"
        else:
            titleOfPets = user_name + "'s " + "pets"

        embed = discord.Embed(title=titleOfPets, description="", color=0xffffff)
        # parse through all of the users pets

        # get their name, types and ids

        array_of_petIDs = user_doc["pets"]
        id_list = ""
        type_list = ""
        name_list = ""

        for petID in array_of_petIDs:
            id_list = id_list + str(petID) + "\n"

            # create the corresponding pet object for this id
            user_pet = read_user_pet(self.db_connection, id, petID)

            # now list its name, along with its type
            type_list = type_list + str(user_pet.type) + "\n"
            name_list = name_list + str(user_pet.name) + "\n"

        # now add it to the embed

        embed.add_field(name="Name ", value=name_list, inline=True)
        embed.add_field(name="Type ", value=type_list, inline=True)
        embed.add_field(name="ID ", value=id_list, inline=True)
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
        user_doc = self.db_connection.profile_find({"id": id})
        if user_doc is None:
            await ctx.send("Please set up your profile first!")
            return
        array_of_petIDs = user_doc["pets"]

        if not (num in array_of_petIDs):
            await ctx.send("Please provide a valid pet ID.")
            return

        pet_obj = read_user_pet(self.db_connection, id, int(idToSwitch))
        # now try to switch their current petID
        self.db_connection.profile_update({"id": id}, {"$set": {"currentPet": int(idToSwitch), "pet": pet_obj.name}})
        await ctx.send("Pet set!")


def setup(client):
    client.add_cog(pet_commands(client, database_connection()))
