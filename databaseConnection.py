import pymongo
# import gridfs
# import secret
import os
from boto.s3.connection import S3Connection


# heroku environment variables
KEY = os.environ['secret_key']


class databaseConnection:

    def __init__(self):
        self.dbclient = pymongo.MongoClient(KEY)
        self.db = self.dbclient.bot

        # allows us in the future to insert actual images in the database:
        # self.fs = gridfs.GridFS(self.db)

    def openDatabase(self):
        # logs onto mongodb's database, we are using the atlas client
        self.dbclient = pymongo.MongoClient(KEY)
        self.db = self.dbclient.bot

    def closeDatabase(self):
        self.dbclient.close()

    # profile
    def profileInsert(self, toInsert):
        self.db.profile.insert(toInsert)

    def profileFind(self, findCriteria):
        return self.db.profile.find_one(findCriteria)

    def profileUpdate(self, updateCritera, change):
        self.db.profile.update(updateCritera, change)


    # server
    def serverInsert(self, toInsert):
        self.db.server.insert(toInsert)

    def serverFind(self, findCriteria):
        return self.db.server.find_one(findCriteria)

    def serverUpdate(self, updateCriteria, change):
        self.db.server.update(updateCriteria, change)

    # pet-outlines
    def getAllPetOutlines(self):
        return self.db.pet_outlines.find({})

    def getSpecificPetOutline(self, findCriteria):
        return self.db.pet_outlines.find_one(findCriteria)


    #user-pets
    '''
    For general information later, user pets will have multiple identifiers
    
    First, they will be identified via the user id who owns them
    Next, they will be identified by their "pet number" in association to an array
    '''
    def getUserPet(self, findCriteria):
        return self.db.user_pets.find_one(findCriteria)

    def deleteUserPet(self, deleteCriteria):
        return

    def updateUserPet(self, updateCriteria, change):
        self.db.user_pets.update(updateCriteria, change)

    def insertUserPet(self, toInsert):
        self.db.user_pets.insert(toInsert)