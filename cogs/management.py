import discord
from discord.ext import commands
from databaseConnection import databaseConnection
from archive.currency import giveMoney


# a general ownerAdminTest any cog should be able to use as long
# as they have a database connection
def ownerAdminTest(ctx, dbConnection):
    id = ctx.author.id

    # they are an admin of the server, let them pass
    if ownerTest(ctx.guild.get_member(id)):
        return True

    user = dbConnection.profileFind({"id": id})
    return adminTest(user)


'''
Takes in a discord member
Returns if they are an administrator of the current server or not
'''


def ownerTest(member):
    return member.guild_permissions.administrator


'''
Takes in a user from the database
Returns if they are a bot administrator or not
'''


def adminTest(user):
    if user is None:
        return False
    try:
        rank = user['rank']
    except KeyError:
        return False

    if rank == "Admin":
        return True

    return False


class management(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection

    @commands.command()
    async def give(self, ctx, user: discord.User, amountToGive):
        num = 0
        try:
            num = int(amountToGive)
        except ValueError:
            msg = "Please provide a valid amount of money to give."
            await ctx.send(msg)
            return

        if num < 0:
            msg = "Please do not give negative knuts."
            await ctx.send(msg)
            return

        result = ownerAdminTest(ctx, self.dbConnection)
        if result is False:
            msg = "You do not have permission to give money."
            await ctx.send(msg)
            return

        userProfile = self.dbConnection.profileFind({"id": user.id})
        if userProfile is None:
            msg = "The person to give to has not yet set up their profile."
            await ctx.send(msg)
            return

        if giveMoney(self.dbConnection, user.id, num):
            msg = "Gave " + userProfile["username"] + " " + str(num) + " knuts."
        else:
            msg = "The person does not have any coin section in their profile."

        await ctx.send(msg)

    @commands.command()
    async def take(self, ctx, user: discord.User, amountToTake):

        num = 0
        try:
            num = int(amountToTake)
        except ValueError:
            msg = "Please provide a valid amount of money to take."
            await ctx.send(msg)
            return

        if num < 0:
            msg = "Please do not take negative knuts."
            await ctx.send(msg)
            return

        result = ownerAdminTest(ctx, self.dbConnection)
        if result is False:
            msg = "You do not have permission to take money."
            await ctx.send(msg)
            return

        userProfile = self.dbConnection.profileFind({"id": user.id})
        if userProfile is None:
            msg = "The person to take from has not yet set up their profile."
            await ctx.send(msg)
            return

        msg = ""

        try:
            userAmount = userProfile["coins"]
            userAmount -= num
            if userAmount < 0:
                msg = "Can not take that many knuts."
                await ctx.send(msg)
                return

            self.dbConnection.profileUpdate({"id": user.id}, {"$set": {"coins": userAmount}})
            msg = "Took from " + userProfile["username"] + " " + str(num) + " knuts."
        except:
            msg = "The person does not have any coin section in their profile."

        await ctx.send(msg)

    @commands.command()
    async def makeVip(self, ctx, user: discord.User):
        result = ownerAdminTest(ctx, self.dbConnection)
        if result is False:
            await ctx.send("You do not have permission to make someone a VIP.")
            return
        else:
            userProfile = self.dbConnection.profileFind({"id": user.id})
            if userProfile is None:
                await ctx.send("The user did not set up their profile!")
                return

            if adminTest(userProfile):
                await ctx.send("You can not demote a fellow admin!")
                return

            # make them a VIP
            self.dbConnection.profileUpdate({"id": user.id}, {"$set": {"rank": "VIP"}})
            await ctx.send("Successfully made them a VIP.")
            pass

    @commands.command()
    async def makeAdmin(self, ctx, user: discord.User):
        current = self.dbConnection.profileFind({"id": ctx.author.id})
        # only admins should be able to make others admins
        result = adminTest(current)

        if result is False:
            await ctx.send("You do not have permission to make someone an Admin.")
            return
        else:
            userProfile = self.dbConnection.profileFind({"id": user.id})
            if userProfile is None:
                await ctx.send("The user did not set up their profile!")
                return
            else:
                self.dbConnection.profileUpdate({"id": user.id}, {"$set": {"rank": "Admin"}})
                await ctx.send("Successfully made them an Admin.")
                pass


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(management(client, database_connection))
    return
