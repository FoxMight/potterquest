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

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself, so return if it is itself

    if message.author == client.user:
        return

    # the following starts up the users profile
    if message.content.startswith('!start'):
        id = message.author.id
        # this initializes their profile and distinguishes it based on their discord id
        db.profile.insert({"id" : id, "coins": 0})
        #creates message and sends
        msg = 'Profile set! Have fun! \nBe sure to choose a house with the !house command.'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!hello'):
        #creates message and sends
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!shop'):
        msg = 'Welcome to the magic shop! There is nothing in here right now.'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!house'):
        id = message.author.id
        # see whats in the message -> adjust the specific persons profile based  on it
        # .update "updates" the profile $ must be used to keep old items
        id = message.author.id
        user = db.profile.find_one({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            if 'Gryffindor' in message.content:
                db.profile.update({"id" : id}, {"$set":{"house": "Gryffindor"}} )
                msg = 'Welcome to the Gryffindor house!'
            elif 'Hufflepuff' in message.content:
                db.profile.update({"id" : id}, {"$set":{"house": "Hufflepuff"}} )
                msg = 'Welcome to the Hufflepuff house!'
            elif 'Slytherin' in message.content:
                db.profile.update({"id" : id}, {"$set":{"house": "Slytherin"}} )
                msg = 'Welcome to the Slytherin house!'
            elif 'Ravenclaw' in message.content:
                db.profile.update({"id" : id}, {"$set":{"house": "Ravenclaw"}} )
                msg = 'Welcome to the Ravenclaw house!'
            else:
                msg = "That house doesn't exist."
        await client.send_message(message.channel, msg)

    if message.content.startswith('!profile'):
        id = message.author.id
        user = db.profile.find_one({"id": id})
        if user is None:
            msg = "You did not initialize your profile! Please initialize your profile."
        else:
            msg = '```'
            try:
                user['house']
                msg = msg +'This is your house: ' + user['house']
            except:
                msg = msg +'You did not pick a house!'

            try:
                user['birthday']
                msg = msg + "\nThis is your birthday: "+ user['birthday']
            except:
                msg = msg +'\nYou did not set a birthday!'
            msg = msg + "\nYou have this many coins: " +str(user['coins']) + ' ```'
            #try:
                #user['bgpic']
                #msg = msg + '\n'
        await client.send_message(message.channel, msg)


    if message.content.startswith('!birthday'):
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

    if message.content.startswith('!picture'):
        with open('D:\\OneDrive\\CS_Projects\\Potterquest\\4WlzSRn.gif', 'rb') as picture:
            await client.send_file(message.channel, picture)

    if message.content.startswith('!cheese'):
        id = message.author.id
        if(id == '93121870949281792'):
            msg = "GIMME MY DAMN CHEESE"
            await client.send_message(message.channel, msg)

    if message.content.startswith('!ariana'):
        id = message.author.id
        if(id == '110586016921862144'):
            with open ('D:\\OneDrive\\CS_Projects\\Potterquest\\image2.jpg', 'rb') as picture:
                 await client.send_file(message.channel, picture)



@client.event
async def on_ready():
    await client.change_presence(game= discord.Game(name='Quidditch'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)

