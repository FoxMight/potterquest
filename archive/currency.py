import discord
from discord.ext import commands
from datetime import datetime, timedelta
from databaseConnection import databaseConnection
from timeManagement import compareTime, storeDateTime, constructDateTime, compareTime


class currency(commands.Cog):

    def __init__(self, client, databaseConnection):
        self.client = client
        self.dbConnection = databaseConnection

    @commands.command()
    async def daily(self, ctx):
        id = ctx.author.id
        currentTime = datetime.now()
        user = self.dbConnection.profileFind({"id": id})

        # check the users time
        try:
            # test the time difference
            oldTime = constructDateTime(user)
            if oldTime is None:
                raise Exception("Error constructing date time.")

            timeDiff = compareTime(oldTime, currentTime)

            # if it has been 24 hours
            if timeDiff < 86400:
                # convert time to wait into a minute hour format
                timeToWait = 86400 - timeDiff

                m, s = divmod(timeToWait, 60)
                h, m = divmod(m, 60)

                msg = "Please wait "
                if h > 0:
                    msg += str(int(h)) + " hour(s), " + str(int(m)) + " minute(s) and " + str(int(s)) + " second(s)."
                elif m > 0:
                    msg += str(int(m)) + " minute(s) and " + str(int(s)) + " second(s)."
                elif s > 0:
                    msg += str(int(s)) + " second(s)."

                await ctx.send(msg)
                return
            else:
                return await self.giveDaily(ctx, currentTime, id)

        except:
            # this is their first time! give them the money
            return await self.giveDaily(ctx, currentTime, id)

    # function to give them the daily coins if their profile has been set up
    async def giveDaily(self, ctx, currentTime, id):
        if not storeDateTime(self.dbConnection, id, currentTime):
            msg = "Please set up your profile first!"
            await ctx.send(msg)
            return
        # give them the money
        if not giveMoney(self.dbConnection, id, 20):
            msg = "Please set up your profile first!"
        else:
            msg = "Received 20 knuts."
        await ctx.send(msg)
        return


def setup(client):
    database_connection = databaseConnection()
    client.add_cog(currency(client, database_connection))
    return


def giveMoney(dbConnection, id, amount):
    if amount < 0:
        return False

    try:
        user = dbConnection.profileFind({"id": id})
        userAmount = user["coins"]
        userAmount += amount
        dbConnection.profileUpdate({"id": id}, {"$set": {"coins": userAmount}})
        return True
    except Exception as e:
        return False
