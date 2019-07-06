import discord
from discord.ext import commands

shop = ['Bear', 'Turtle']
cost = [500, 500]

class shopCommands(commands.Cog):
    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Ye old magic shop", description="", color=0xFFDF00)
        #get the entire pet list
        costs = ""
        items = ""
        i = 0

        while i < len(shop):
            items = items + shop[i] + "\n"
            costs = costs + str(cost[i]) + " knuts\n"
            i += 1

        embed.add_field(name="Pets: \n", value="Look at our magical pets for sale!", inline=False)
        embed.add_field(name="Name ", value=items, inline=True)
        embed.add_field(name="Cost ", value=costs, inline=True)

        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(shopCommands(client))