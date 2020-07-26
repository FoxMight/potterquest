import pymongo
# import gridfs
import secret


class database_connection:

    def __init__(self):
        self.db_client = pymongo.MongoClient(secret.secret_key)
        self.db = self.db_client.bot

        # allows us in the future to insert actual images in the database:
        # self.fs = gridfs.GridFS(self.db)

    def open_database(self):
        # logs onto mongodb's database, we are using the atlas client
        self.db_client = pymongo.MongoClient(secret.secret_key)
        self.db = self.db_client.bot

    def close_database(self):
        self.db_client.close()

    # profile
    def profile_insert(self, to_insert):
        self.db.profile.insert(to_insert)

    def profile_find(self, find_criteria):
        return self.db.profile.find_one(find_criteria)

    def profile_update(self, update_criteria, change):
        self.db.profile.update(update_criteria, change)

    # server
    def server_insert(self, to_insert):
        self.db.server.insert(to_insert)

    def server_find(self, find_criteria):
        return self.db.server.find_one(find_criteria)

    def server_update(self, update_criteria, change):
        self.db.server.update(update_criteria, change)

    # pet-outlines
    def get_all_pet_outlines(self):
        return self.db.pet_outlines.find({})

    def get_specific_pet_outline(self, findCriteria):
        return self.db.pet_outlines.find_one(findCriteria)

    # user-pets
    """
    For general information later, user pets will have multiple identifiers
    
    First, they will be identified via the user id who owns them
    Next, they will be identified by their "pet number" in association to an array
    """

    def get_user_pet(self, find_criteria):
        return self.db.user_pets.find_one(find_criteria)

    def delete_user_pet(self, delete_criteria):
        return

    def update_user_pet(self, update_criteria, change):
        self.db.user_pets.update(update_criteria, change)

    def insert_user_pet(self, to_insert):
        self.db.user_pets.insert(to_insert)
