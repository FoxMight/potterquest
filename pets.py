import discord
from discord.ext import commands
from database_connection import database_connection
import copy


class Pet:

    def __init__(self, type, cost, picture, name=None, pet_id=None, user_id=None):
        if pet_id is None:
            pet_id = -1
        if user_id is None:
            user_id = -1
        if name is None:
            name = type
        self.type = type
        self.name = name
        self.cost = cost
        self.picture = picture
        self.link = picture
        self.pet_id = pet_id
        self.user_id = user_id
        return


def save_pet(db_connection: database_connection, pet: Pet) -> object:
    if pet.user_id < 0 or pet.pet_id < 0:
        return False

    # first check if the pet already exists
    petDoc = db_connection.get_user_pet({"userID": pet.user_id, "petID": pet.pet_id})
    if petDoc is None:
        # the pet has not been created yet
        # insert it as a new document
        db_connection.insert_user_pet({"userID": pet.user_id, "petID": pet.pet_id, "Type": pet.type,
                                      "Nickname": pet.name, "Picture": pet.picture, "Cost": pet.cost})

    else:
        # update the current pets information
        db_connection.update_user_pet({"userID": pet.user_id, "petID": pet.pet_id},
                                      {"userID": pet.user_id, "petID": pet.pet_id, "Type": pet.type,
                                      "Nickname": pet.name, "Picture": pet.picture, "Cost": pet.cost})

    return True


def read_pet_outline(db_connection):
    allPets = db_connection.get_all_pet_outlines()
    listOfPets = {}
    for petDoc in allPets:
        newPet = Pet(petDoc["Type"], petDoc["Cost"], petDoc["Picture"])
        listOfPets.update({petDoc["Type"]: newPet})

    return listOfPets


def read_user_pet(db_connection, userID, petID):
    petDoc = db_connection.get_user_pet({"userID": userID, "petID": petID})

    if petDoc is None:
        return None

    newPet = Pet(petDoc["Type"], petDoc["Cost"], petDoc["Picture"], petDoc["Nickname"], petDoc["petID"],
                 petDoc["userID"])
    return newPet


def update_pet_details(db_connection, user_doc, user_id, users_pet):
    new_pet_id = user_doc["petIDCount"]
    new_pet_id += 1
    users_pet.user_id = user_id
    users_pet.pet_id = new_pet_id
    # update the users petIDCount and their pet array
    db_connection.profile_update({"id": user_id}, {"$set": {"petIDCount": new_pet_id}})
    # and point their profile to that pet
    db_connection.profile_update({"id": user_id}, {"$push": {"pets": new_pet_id}})


def generate_pet(db_connection, pet_name, user_doc, id):
    petObj = read_specific_pet_outline(db_connection, pet_name)
    usersPet = copy.copy(petObj)
    update_pet_details(db_connection, user_doc, id, usersPet)
    save_pet(db_connection, usersPet)


def read_specific_pet_outline(db_connection, name):
    pet_doc = db_connection.get_specific_pet_outline({"Type": name})
    new_pet: Pet = Pet(pet_doc["Type"], pet_doc["Cost"], pet_doc["Picture"])
    return new_pet

# def readPetStructure(dbConnection, type):
#     """
#
#     :type dbConnection:databaseConnection
#     :type type:str
#
#     :return: a pet object if we found the outline for a pet, none if we failed to find the
#     outline
#     """
#
#     petDoc = dbConnection.getSpecificPetOutline({"Type": type})
#     if petDoc is None:
#         return None
#     else:
#         return pet(petDoc["Type"], petDoc["Cost"], petDoc["Picture"])
