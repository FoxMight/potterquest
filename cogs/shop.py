import discord
from discord.ext import commands
from pets import Pet, read_pet_outline, save_pet, update_pet_details
from database_connection import database_connection
import copy


class shop_commands(commands.Cog):

    def __init__(self, client, inner_database_connection):
        self.client = client
        self.database_connection = inner_database_connection
        self.pets = read_pet_outline(inner_database_connection)
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
            costs = costs + str(petObj.cost) + " knuts\n"
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
            pet_obj = self.pets[name]
            if pet_obj is None:
                await ctx.send("That pet is not in the shop yet!")
                return

            # check how much money the user has

            userID = ctx.author.id

            # see if the user exists in the database
            user_doc = self.database_connection.profile_find({"id": userID})
            if user_doc is None:
                await ctx.send("Please set up your profile first!")
                return

            user_coins = user_doc["coins"]

            if pet_obj.cost > user_coins:
                await ctx.send("You do not have enough money to buy that!")
                return
            user_coins = user_coins - pet_obj.cost
            # we already have a pet outline for the pet
            # and the userid, we just need to give the pet outline copy
            users_pet = copy.copy(pet_obj)
            update_pet_details(self.database_connection, user_doc, userID, users_pet)
            # save the pet
            save_pet(self.database_connection, users_pet)

            # letters in vowel as a list
            vowels = ["a", "e", "i", "o", "u"]
            if (pet_obj.type)[0].lower() in vowels:
                msg = "Buying an " + pet_obj.type + "!"
            else:
                msg = "Buying a " + pet_obj.type + "!"
            self.database_connection.profile_update({"id": userID}, {"$set": {"coins": user_coins}})
        else:
            msg = "Please provide a valid set to buy from!"

        await ctx.send(msg)


def setup(client):
    client.add_cog(shop_commands(client, database_connection()))
