import pymongo
# import gridfs
import secret


class databaseConnection:

    def __init__(self):
        self.dbclient = pymongo.MongoClient(secret.secret_key)
        self.db = self.dbclient.bot

        # allows us in the future to insert actual images in the database:
        # self.fs = gridfs.GridFS(self.db)

    def openDatabase(self):
        # logs onto mongodb's database, we are using the atlas client
        self.dbclient = pymongo.MongoClient(secret.secret_key)
        self.db = self.dbclient.bot

    def closeDatabase(self):
        self.dbclient.close()

    def profileInsert(self, toInsert):
        self.db.profile.insert(toInsert)

    def profileFind(self, findCriteria):
        return self.db.profile.find_one(findCriteria)

    def profileUpdate(self, updateCritera, change):
        self.db.profile.update(updateCritera, change)
