import discord
from discord.ext import commands
from database_connection import database_connection
from pets import read_specific_pet_outline, Pet, update_pet_details, save_pet, generate_pet
import copy


class profileSetup(commands.Cog):

    def __init__(self, client, inner_database_connection):
        self.client = client
        self.database_connection = inner_database_connection

    #   A command all users must use in order to start their database profile up
    #   It is possible to force them to immediately choose a house, but I decided
    #   this would be better
    @commands.command()
    async def start(self, ctx):
        id = ctx.author.id

        profile = self.database_connection.profile_find({"id": id})
        if profile is not None:
            msg = 'You have already set your profile! You can not set it again.'
            await ctx.send(msg)
            return

        name = ctx.author.name
        # this initializes their profile and distinguishes it based on their discord id
        self.database_connection.profile_insert({"id": id, "coins": 0, "username": name,
                                         "rank": "Regular", "petIDCount": -1, "currentPet": -1,
                                         "pets": []})

        # creates message and sends
        msg = 'Profile set! Have fun! \nBe sure to choose a house with the +house command.'
        await ctx.send(msg)

    #   If a user sends "+nameUpdate" in the chat, the bot automatically updates the users
    #   stored username to what it current is
    #   It will not save anything if the user is not yet initialized in the database
    @commands.command()
    async def name_update(self, ctx, *, userName):
        id = ctx.author.id

        user = self.database_connection.profile_find({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            msg = "Username set!"
            self.database_connection.profile_update({"id": id}, {"$set": {"username": userName}})

        await ctx.send(msg)

    @commands.command()
    async def house(self, ctx, *, houseName):
        houseName = houseName.lower()
        # see whats in the message -> adjust the specific persons profile based  on it
        # .update "updates" the profile $ must be used to keep old items
        id = ctx.author.id
        user = self.database_connection.profile_find({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            try:
                user['house']
                if user['house'] == "Gryffindor":
                    msg = "You are already in the Gryffindor house"
                elif user['house'] == "Ravenclaw":
                    msg = "You are already in the Ravenclaw house."
                elif user['house'] == "Hufflepuff":
                    msg = "You are already in the Hufflepuff house."
                elif user['house'] == "Slytherin":
                    msg = "You are already in the Slytherin house."
            except:
                if 'gryffindor' in houseName:
                    petName = "Lion"
                    generate_pet(self.database_connection, petName, user, id)
                    self.database_connection.profile_update({"id": id}, {"$set": {"house": "Gryffindor"}})
                    msg = 'Welcome to the Gryffindor house!\nFor joining Gryffidor house you have received a Lion!'

                elif 'hufflepuff' in houseName:
                    petName = "Honey Badger"
                    generate_pet(self.database_connection, petName, user, id)
                    self.database_connection.profile_update({"id": id},
                                                            {"$set": {"house": "Hufflepuff"}})
                    msg = 'Welcome to the Hufflepuff house!\nFor joining the Hufflepuff house you have received a ' \
                          'Honey Badger! '
                elif 'slytherin' in houseName:
                    petName = "Snake"
                    generate_pet(self.database_connection, petName, user, id)
                    self.database_connection.profile_update({"id": id}, {"$set": {"house": "Slytherin"}})
                    msg = 'Welcome to the Slytherin house!\nFor joining the Slytherin house you have recieved a Snake!'
                elif 'ravenclaw' in houseName:
                    petName = "Eagle"
                    generate_pet(self.database_connection, petName, user, id)
                    self.database_connection.profile_update({"id": id}, {"$set": {"house": "Ravenclaw"}})
                    msg = 'Welcome to the Ravenclaw house!\nFor joining the Ravenclaw house you have recieved an Eagle!'
                else:
                    msg = "That house doesn't exist."
        await ctx.send(msg)

    #   Goes through certain elements of a users data in the database
    #   and puts them into an embed to send to the user through the bot
    @commands.command()
    async def profile(self, ctx):
        id = ctx.author.id
        name = ctx.author.name
        user = self.database_connection.profile_find({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
            await ctx.send(msg)
        else:
            try:
                name = user['username']
            except:
                pass
            try:
                user['house']
                if user['house'] == "Gryffindor":
                    embed = discord.Embed(title=name, description="", color=0xff1300)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(
                        url="https://vignette.wikia.nocookie.net/gamekillers-rpgs/images/9/93/Gryffindor_Icon.png/revision/latest?cb=20160124110732")
                elif user['house'] == "Ravenclaw":
                    embed = discord.Embed(title=name, description="", color=0x0d02d0)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(
                        url="https://vignette.wikia.nocookie.net/harrypotter/images/4/4e/RavenclawCrest.png/revision/latest/scale-to-width-down/350?cb=20161020182442")
                elif user['house'] == "Hufflepuff":
                    embed = discord.Embed(title=name, description="", color=0xfff45c)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(
                        url="https://vignette.wikia.nocookie.net/harrypotter/images/0/06/Hufflepuff_ClearBG.png/revision/latest?cb=20161020182518")
                elif user['house'] == "Slytherin":
                    embed = discord.Embed(title=name, description="", color=0x02a650)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(
                        url="https://vignette.wikia.nocookie.net/cour-de-cassation/images/0/00/Slytherin_ClearBG.png/revision/latest?cb=20190414174141")
                else:
                    embed = discord.Embed(title=name, description="", color=0xffffff)
                    embed.add_field(name="House", value="N/A", inline=False)
            except:
                embed = discord.Embed(title=name, description="", color=0xffffff)
                embed.add_field(name="House", value="N/A", inline=False)

            try:
                user['birthday']
                embed.add_field(name="Birthday", value=user['birthday'], inline=False)
            except:
                embed.add_field(name="Birthday", value="N/A", inline=False)

            try:
                user['pet']
                embed.add_field(name="Pet", value=user['pet'], inline=False)
            except:
                embed.add_field(name="Pet", value="N/A", inline=False)

            try:
                user['rank']
                embed.add_field(name="Rank", value=user['rank'], inline=False)
            except:
                embed.add_field(name="Rank", value="N/A", inline=False)

            embed.add_field(name="Berries", value=user['coins'], inline=False)

            try:
                user['picture']
                embed.set_image(url=user['picture'])
            except:
                # nothing
                embed.Empty
            await ctx.send(embed=embed)

    #   Given a users profile picture as a url link
    #   inserts it into their profile!
    @commands.command()
    async def setpfp(self, ctx, *, picture):
        id = ctx.author.id
        user = self.database_connection.profile_find({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            if "https" in picture:
                self.database_connection.profile_update({"id": id}, {"$set": {"picture": picture}})
                msg = 'Picture saved'
            else:
                msg = 'Invalid picture format'

        await ctx.send(msg)

    @commands.command()
    async def birthday(self, ctx, *, birthday):
        # lets get the users birthday!
        id = ctx.author.id
        user = self.database_connection.profile_find({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            self.database_connection.profile_update({"id": id}, {"$set": {"birthday": birthday}})
            msg = 'Birthday saved'
        await ctx.send(msg)

    @commands.command()
    async def berries(self, ctx):
        # lets get the users coins!
        id = ctx.author.id
        user = self.database_connection.profile_find({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            msg = 'You have ' + str(user['coins']) + ' berries.'
        await ctx.send(msg)


def setup(client):
    client.add_cog(profileSetup(client, database_connection()))
