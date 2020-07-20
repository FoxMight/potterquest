import pymongo
# import gridfs
import secret


class database_connection:

    def __init__(self):
        self.dbclient = pymongo.MongoClient(secret.secret_key)
        self.db = self.dbclient.bot

        # allows us in the future to insert actual images in the database:
        # self.fs = gridfs.GridFS(self.db)

    def open_database(self):
        # logs onto mongodb's database, we are using the atlas client
        self.dbclient = pymongo.MongoClient(secret.secret_key)
        self.db = self.dbclient.bot

    def close_database(self):
        self.dbclient.close()

    # profile
    def profile_insert(self, toInsert):
        self.db.profile.insert(toInsert)

    def profile_find(self, findCriteria):
        return self.db.profile.find_one(findCriteria)

    def profile_update(self, updateCritera, change):
        self.db.profile.update(updateCritera, change)


    # server
    def server_insert(self, toInsert):
        self.db.server.insert(toInsert)

    def server_find(self, findCriteria):
        return self.db.server.find_one(findCriteria)

    def server_update(self, updateCriteria, change):
        self.db.server.update(updateCriteria, change)

    # pet-outlines
    def get_all_pet_outlines(self):
        return self.db.pet_outlines.find({})

    def get_specific_pet_outline(self, findCriteria):
        return self.db.pet_outlines.find_one(findCriteria)


    #user-pets
    '''
    For general information later, user pets will have multiple identifiers
    
    First, they will be identified via the user id who owns them
    Next, they will be identified by their "pet number" in association to an array
    '''
    def get_user_pet(self, findCriteria):
        return self.db.user_pets.find_one(findCriteria)

    def delete_user_pet(self, deleteCriteria):
        return

    def update_user_pet(self, updateCriteria, change):
        self.db.user_pets.update(updateCriteria, change)

    def insert_user_pet(self, toInsert):
        self.db.user_pets.insert(toInsert)