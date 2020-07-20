import discord
from discord.ext import commands
from database_connection import database_connection
import copy


class pet:

    def __init__(self, type, cost, picture, name=None, petID=None, userID=None):
        if petID is None:
            petID = -1
        if userID is None:
            userID = -1
        if name is None:
            name = type
        self.type = type
        self.name = name
        self.cost = cost
        self.picture = picture
        self.link = picture
        self.petID = petID
        self.userID = userID
        return


def savePet(dbConnection, pet):
    if pet.userID < 0 or pet.petID < 0:
        return False

    # first check if the pet already exists
    petDoc = dbConnection.get_user_pet({"userID": pet.userID, "petID": pet.petID})
    if petDoc is None:
        # the pet has not been created yet
        # insert it as a new document
        dbConnection.insert_user_pet({"userID": pet.userID, "petID": pet.petID, "Type": pet.type,
                                    "Nickname": pet.name, "Picture": pet.picture, "Cost": pet.cost})

    else:
        # update the current pets information
        dbConnection.update_user_pet({"userID": pet.userID, "petID": pet.petID},
                                     {"userID": pet.userID, "petID": pet.petID, "Type": pet.type,
                                    "Nickname": pet.name, "Picture": pet.picture, "Cost": pet.cost})

    return True


def readPetOutline(dbConnection):
    allPets = dbConnection.get_all_pet_outlines()
    listOfPets = {}
    for petDoc in allPets:
        newPet = pet(petDoc["Type"], petDoc["Cost"], petDoc["Picture"])
        listOfPets.update({petDoc["Type"]: newPet})

    return listOfPets

def read_user_pet(dbConnection, userID, petID):

    petDoc = dbConnection.get_user_pet({"userID": userID, "petID": petID})

    if petDoc is None:
        return None

    newPet = pet(petDoc["Type"], petDoc["Cost"], petDoc["Picture"], petDoc["Nickname"], petDoc["petID"],
                 petDoc["userID"])
    return newPet


def updatePetDetails(dbConnection, userDoc, userID, usersPet):
    newPetID = userDoc["petIDCount"]
    newPetID += 1
    usersPet.userID = userID
    usersPet.petID = newPetID
    # update the users petIDCount and their pet array
    dbConnection.profile_update({"id": userID}, {"$set": {"petIDCount": newPetID}})
    # and point their profile to that pet
    dbConnection.profile_update({"id": userID}, {"$push": {"pets": newPetID}})


def generate_pet(dbConnection, petName, userDoc, id):
    petObj = readSpecificPetOutline(dbConnection, petName)
    usersPet = copy.copy(petObj)
    updatePetDetails(dbConnection, userDoc, id, usersPet)
    savePet(dbConnection, usersPet)

def readSpecificPetOutline(dbConnection, name):
    petDoc = dbConnection.get_specific_pet_outline({"Type": name})
    newPet = pet(petDoc["Type"], petDoc["Cost"], petDoc["Picture"])
    return newPet


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
