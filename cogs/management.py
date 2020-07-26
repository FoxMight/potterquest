import discord
from discord.ext import commands
from database_connection import database_connection
from .currency import give_money


# a general ownerAdminTest any cog should be able to use as long
# as they have a database connection
def owner_admin_test(ctx, db_connection) -> bool:
    """
    Checks if the author of the current message context has admin rights in the databse
    ownership rights in this server

    :param ctx: The context
    :param db_connection: The database connection
    :return:
    """
    id = ctx.author.id

    # they are an admin of the server, let them pass
    if owner_test(ctx.guild.get_member(id)):
        return True

    user = db_connection.profile_find({"id": id})
    return admin_test(user)


'''
Takes in a discord member
Returns if they are an administrator of the current server or not
'''
def owner_test(member: discord.Member) -> bool:
    """
    :param member: The discord member to to check if they have ownership rights in their server
    :return: Whether or not they have admin rights
    """
    return member.guild_permissions.administrator


def admin_test(user) -> bool:
    """
    :param user: A dictionary containing the users information
    :return: Whether or not they have admin privileges in the bot
    """
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

    def __init__(self, client, inner_database_connection):
        self.client = client
        self.db_connection = inner_database_connection

    @commands.command()
    async def give(self, ctx, user: discord.User, amount_to_give):
        num = 0
        try:
            num = int(amount_to_give)
        except ValueError:
            msg = "Please provide a valid amount of money to give."
            await ctx.send(msg)
            return

        if num < 0:
            msg = "Please do not give negative knuts."
            await ctx.send(msg)
            return

        result = owner_admin_test(ctx, self.db_connection)
        if result is False:
            msg = "You do not have permission to give money."
            await ctx.send(msg)
            return

        userProfile = self.db_connection.profile_find({"id": user.id})
        if userProfile is None:
            msg = "The person to give to has not yet set up their profile."
            await ctx.send(msg)
            return

        if give_money(self.db_connection, user.id, num):
            msg = "Gave " + userProfile["username"] + " " + str(num) + " knuts."
        else:
            msg = "The person does not have any coin section in their profile."

        await ctx.send(msg)

    @commands.command()
    async def take(self, ctx, user: discord.User, amount_to_take):

        num = 0
        try:
            num = int(amount_to_take)
        except ValueError:
            msg = "Please provide a valid amount of money to take."
            await ctx.send(msg)
            return

        if num < 0:
            msg = "Please do not take negative knuts."
            await ctx.send(msg)
            return

        result = owner_admin_test(ctx, self.db_connection)
        if result is False:
            msg = "You do not have permission to take money."
            await ctx.send(msg)
            return

        user_profile = self.db_connection.profile_find({"id": user.id})
        if user_profile is None:
            msg = "The person to take from has not yet set up their profile."
            await ctx.send(msg)
            return

        msg = ""

        try:
            userAmount = user_profile["coins"]
            userAmount -= num
            if userAmount < 0:
                msg = "Can not take that many knuts."
                await ctx.send(msg)
                return

            self.db_connection.profile_update({"id": user.id}, {"$set": {"coins": userAmount}})
            msg = "Took from " + user_profile["username"] + " " + str(num) + " knuts."
        except:
            msg = "The person does not have any coin section in their profile."

        await ctx.send(msg)

    @commands.command()
    async def make_vip(self, ctx, user: discord.User):
        result = owner_admin_test(ctx, self.db_connection)
        if result is False:
            await ctx.send("You do not have permission to make someone a VIP.")
            return
        else:
            userProfile = self.db_connection.profile_find({"id": user.id})
            if userProfile is None:
                await ctx.send("The user did not set up their profile!")
                return

            if admin_test(userProfile):
                await ctx.send("You can not demote a fellow admin!")
                return

            # make them a VIP
            self.db_connection.profile_update({"id": user.id}, {"$set": {"rank": "VIP"}})
            await ctx.send("Successfully made them a VIP.")
            pass

    @commands.command()
    async def make_admin(self, ctx, user: discord.User):
        current = self.db_connection.profile_find({"id": ctx.author.id})
        # only admins should be able to make others admins
        result = admin_test(current)

        if result is False:
            await ctx.send("You do not have permission to make someone an Admin.")
            return
        else:
            user_profile = self.db_connection.profile_find({"id": user.id})
            if user_profile is None:
                await ctx.send("The user did not set up their profile!")
                return
            else:
                self.db_connection.profile_update({"id": user.id}, {"$set": {"rank": "Admin"}})
                await ctx.send("Successfully made them an Admin.")
                return


def setup(client):
    client.add_cog(management(client, database_connection()))
    return
