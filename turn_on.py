import discord
import asyncio
import pymongo

# logs onto mongodb's database, we are using the atlas client DO NOT USE MY PASSWORD PLEASE
dbclient = pymongo.MongoClient('mongodb+srv://kironb:NotADBMRut#9%3@cluster0-5ci6q.mongodb.net/test?retryWrites=true')
db = dbclient.bot

# use later, the following is to insert into the database
#db.profile.insert({"age": 19, "name": "Kris"})

TOKEN = 'NDk5NjU0Njc5NjQzNDIyNzMx.DqD2fw.ikcwV55z8PnGvTLWiEno8Jbgi38'

# the following finds the first profile, adjust this to be better

# initializing discord client
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself, so return if it is itself

    if message.author == client.user:
        return

    if message.content.startswith('!start'):
        id = message.author.id
        db.profile.insert({"id" : id})
        msg = 'Profile set! Have fun! \nBe sure to choose a house with the !house command.'
        await client.send_message(message.channel, msg)


    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!house'):
        id = message.author.id
        if 'Gryffindor' in message.content:
            db.profile.update({"id" : id}, {"$set":{"house": "Gryffindor"}} )
            msg = 'Welcome to the Gryffindor house!'
            await client.send_message(message.channel, msg)
        elif 'Hufflepuff' in message.content:
            db.profile.update({"id" : id}, {"$set":{"house": "Hufflepuff"}} )
            msg = 'Welcome to the Hufflepuff house!'
            await client.send_message(message.channel, msg)
        elif 'Slytherin' in message.content:
            db.profile.update({"id" : id}, {"$set":{"house": "Slytherin"}} )
            msg = 'Welcome to the Slytherin house!'
            await client.send_message(message.channel, msg)
        elif 'Ravenclaw' in message.content:
            db.profile.update({"id" : id}, {"$set":{"house": "Ravenclaw"}} )
            msg = 'Welcome to the Ravenclaw house!'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!profile'):
        id = message.author.id
        user = db.profile.find_one({"id": id})
        msg = ' ```This is your house: ' + user['house'] + "\nThis is your birthday: "+ user['birthday'] +"```"
        await client.send_message(message.channel, msg)

    if message.content.startswith('!birthday'):
        #lets get the users birthday!
        id = message.author.id
        birthday = message.content[9:]
        db.profile.update({"id" : id}, {"$set":{"birthday": birthday}} )
        msg = 'Birthday saved'
        await client.send_message(message.channel, msg)



@client.event
async def on_ready():
    await client.change_presence(game= discord.Game(name='Quidditch'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)

