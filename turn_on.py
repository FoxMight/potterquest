import discord
import asyncio
import pymongo
import gridfs

# logs onto mongodb's database, we are using the atlas client DO NOT USE MY PASSWORD PLEASE
dbclient = pymongo.MongoClient('mongodb+srv://kironb:NotADBMRut#9%3@cluster0-5ci6q.mongodb.net/test?retryWrites=true')
db = dbclient.bot

fs = gridfs.GridFS(db)

# use later, the following is to insert into the database
#db.profile.insert({"age": 19, "name": "Kris"})

TOKEN = 'NDk5NjU0Njc5NjQzNDIyNzMx.DqD2fw.ikcwV55z8PnGvTLWiEno8Jbgi38'


# the following finds the first profile, adjust this to be better

# initializing discord client
client = discord.Client()
shop = ['Bear']
cost = [500]
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself, so return if it is itself

    if message.author == client.user:
        return
    
    # the following starts up the users profile
    if message.content.startswith('+help'):
        embed = discord.Embed(title="Help", description="The general list of commands", color=0xFFFFFF)
        embed.add_field(name="Basic Commands", value="+help \n +start (generates a profile)\n +shop  ", inline=False)
        embed.add_field(name="Commands that require a profile", value="+profile \n +coins \n +birthday \n +house \n+setpfp ", inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('+start'):
        id = message.author.id
        # this initializes their profile and distinguishes it based on their discord id
        db.profile.insert({"id" : id, "coins": 0})
        #creates message and sends
        msg = 'Profile set! Have fun! \nBe sure to choose a house with the +house command.'
        await client.send_message(message.channel, msg)

    if message.content.startswith('+hello'):
        #creates message and sends
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('+shop'):
        #msg = 'Welcome to the magic shop! There is nothing in here right now.'
        embed = discord.Embed(title="Ye old magic shop", description="", color=0xFFDF00)
        #get the entire pet list
        costs = ""
        items = ""
        i = 0

        while i <len(shop):
            items = items + shop[i] + "\n"
            costs = costs + str(cost[i]) + " knuts\n"

            i += 1

        embed.add_field(name="Pets: \n", value="Look at our magical pets for sale!", inline=False)
        embed.add_field(name="Name ", value=items, inline=True)
        embed.add_field(name="Cost ", value=costs, inline=True)

        await client.send_message(message.channel, embed=embed)


    if message.content.startswith('+house'):
        id = message.author.id
        # see whats in the message -> adjust the specific persons profile based  on it
        # .update "updates" the profile $ must be used to keep old items
        id = message.author.id
        user = db.profile.find_one({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            try:
                user['house']
                if(user['house'] == "Gryffindor"):
                    msg = "You are already in the Gryffindor house"
                elif(user['house'] == "Ravenclaw"):
                    msg = "You are already in the Ravenclaw house."
                elif(user['house'] == "Hufflepuff" ):
                    msg = "You are already in the Hufflepuff house."
                elif(user['house'] == "Slytherin"):
                    msg = "You are already in the Slytherin house."


            except:
                if 'gryffindor' in message.content.lower():
                    db.profile.update({"id" : id}, {"$set":{"house": "Gryffindor"}} )
                    db.profile.update({"id" : id}, {"$set":{"pet": "Lion" }} )
                    msg = 'Welcome to the Gryffindor house!\nFor joining Gryffidor house you have received a Lion!'
                elif 'hufflepuff' in message.content.lower():
                    db.profile.update({"id" : id}, {"$set":{"house": "Hufflepuff"}} )
                    db.profile.update({"id" : id}, {"$set":{"pet": "Honey Badger" }} )
                    msg = 'Welcome to the Hufflepuff house!\nFor joining the Hufflepuff house you have received a Honey Badger!'
                elif 'slytherin' in message.content.lower():
                    db.profile.update({"id" : id}, {"$set":{"house": "Slytherin"}} )
                    db.profile.update({"id" : id}, {"$set":{"pet": "Snake" }} )
                    msg = 'Welcome to the Slytherin house!\nFor joining the Slytherin house you have recieved a Snake!'
                elif 'ravenclaw' in message.content.lower():
                    db.profile.update({"id" : id}, {"$set":{"house": "Ravenclaw"}} )
                    db.profile.update({"id" : id}, {"$set":{"pet": "Eagle" }} )
                    msg = 'Welcome to the Ravenclaw house!\nFor joining the Ravenclaw house you have recieved an Eagle!'
                else:
                    msg = "That house doesn't exist."
        await client.send_message(message.channel, msg)

    if message.content.startswith('+profile'):
        id = message.author.id
        name = message.author.name
        user = db.profile.find_one({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
            await client.send_message(message.channel, msg)
        else:

            try:
                user['house']
                if(user['house'] == "Gryffindor"):
                    embed = discord.Embed(title=name, description="", color=0xb00800)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/gamekillers-rpgs/images/9/93/Gryffindor_Icon.png/revision/latest?cb=20160124110732")
                elif(user['house'] == "Ravenclaw"):
                    embed = discord.Embed(title=name, description="", color=0x0d02d0)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/harrypotter/images/2/29/0.41_Ravenclaw_Crest_Transparent.png/revision/latest?cb=20161020182442")
                elif(user['house'] == "Hufflepuff" ):
                    embed = discord.Embed(title=name, description="", color=0xfff45c)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/harrypotter/images/5/50/0.51_Hufflepuff_Crest_Transparent.png/revision/latest?cb=20161020182518")
                elif(user['house'] == "Slytherin"):
                    embed = discord.Embed(title=name, description="", color=0x02a650)
                    embed.add_field(name="House", value=user['house'], inline=False)
                    embed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/harrypotter/images/d/d3/0.61_Slytherin_Crest_Transparent.png/revision/latest/scale-to-width-down/700?cb=20161020182557")
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

            embed.add_field(name="Knuts", value=user['coins'], inline=False)

            try:
                user['picture']
                embed.set_image(url = user['picture'])
            except:
                #nothing
                embed.Empty
            await client.send_message(message.channel, embed=embed)
            #try:
                #user['bgpic']
                #msg = msg + '\n'



    if message.content.startswith('+birthday'):
        #lets get the users birthday!
        id = message.author.id
        user = db.profile.find_one({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            birthday = message.content[9:]
            db.profile.update({"id" : id}, {"$set":{"birthday": birthday}} )
            msg = 'Birthday saved'
        await client.send_message(message.channel, msg)

    if message.content.startswith('+picture'):
        with open('D:\\OneDrive\\CS_Projects\\Potterquest\\4WlzSRn.gif', 'rb') as picture:
            await client.send_file(message.channel, picture)

    if message.content.startswith('+cheese'):
        id = message.author.id
        if(id == '93121870949281792'):
            msg = "GIMME MY DAMN CHEESE"
            await client.send_message(message.channel, msg)

    if message.content.startswith('+ariana'):
        id = message.author.id
        if(id == '110586016921862144'):
            with open ('D:\\OneDrive\\CS_Projects\\Potterquest\\image2.jpg', 'rb') as picture:
                 await client.send_file(message.channel, picture)

    if message.content.startswith('+setpfp'):
        id = message.author.id
        user = db.profile.find_one({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            picture = message.content[7:]
            if "https" in picture:
                db.profile.update({"id" : id}, {"$set":{"picture": picture}} )
                msg = 'Picture saved'
            else:
                msg = 'Invalid picture format'
        await client.send_message(message.channel, msg)





@client.event
async def on_ready():
    await client.change_presence(game= discord.Game(name='Quidditch'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)

