from typing import Any

import discord
from discord.ext import commands
from datetime import datetime, timedelta
from database_connection import database_connection
from time_management import compare_time, store_date_time, construct_date_time


class currency(commands.Cog):

    def __init__(self, client, inner_database_connection):
        self.client = client
        self.db_connection = inner_database_connection

    @commands.command()
    async def daily(self, ctx):
        id = ctx.author.id
        current_time: datetime = datetime.now()
        user = self.db_connection.profile_find({"id": id})

        # check the users time
        try:
            # test the time difference
            previous_time = construct_date_time(user)
            if previous_time is None:
                raise Exception("Error constructing date time.")

            time_diff = compare_time(previous_time, current_time)

            # if it has been 24 hours
            if time_diff < 86400:
                # convert time to wait into a minute hour format
                time_to_wait = 86400 - time_diff

                m, s = divmod(time_to_wait, 60)
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
                return await self.give_daily(ctx, current_time, id)

        except Exception as e:
            # this is their first time! give them the money
            return await self.give_daily(ctx, current_time, id)

    # function to give them the daily coins if their profile has been set up
    async def give_daily(self, ctx, current_time, id):
        if not store_date_time(self.db_connection, id, current_time):
            msg = "Please set up your profile first!"
            await ctx.send(msg)
            return
        # give them the money
        if not give_money(self.db_connection, id, 20):
            msg = "Please set up your profile first!"
        else:
            msg = "Received 20 knuts."
        await ctx.send(msg)
        return


def give_money(db_connection: database_connection, id, amount: int) -> bool:
    if amount < 0:
        return False
    try:
        user = db_connection.profile_find({"id": id})
        user_amount = user["coins"]
        user_amount += amount
        db_connection.profile_update({"id": id}, {"$set": {"coins": user_amount}})
        return True
    except Exception as e:
        return False


def setup(client):
    client.add_cog(currency(client, database_connection()))
    return
