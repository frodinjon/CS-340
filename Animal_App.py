# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the bones of an Animal App MongoDB interface.
Our instructions said that it just had to offer the functionality of
reading and writing, but that was tough to test with multiple pieces of data.
I wrote a quick UI (I know it will go away when we build the front end) to 
supply data for searches and for writing. I confirmed this works with both
the sample data provided for each as well as the user input data.
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
#import unittest

print('Hello - Welcome to the Animal Application')
#globally needed variables
userCreateData = {}   #houses input data for write function
userSearchTarget = {}  #houses target data for search function
userUpdateFromTarget = {}  #houses update data for update function
userUpdateToTarget = {}  #houses update data for update function
userDeleteTarget = {}  #houses delete data for delete function
#class
class AnimalShelter(object):
    """CRUD Operations for Animal collection in MongoDB"""
    def __init__(self, user, password):
            # Initializing the MongoClient. This helps to
            # access the MongoDB databases and collections.
            self.client = MongoClient('mongodb://%s:%s@localhost:33853/AAC' % (user, password))
            self.database = self.client['AAC']

    #obtain create data from user
    def obtainCreateData(self):
        #table to ensure data dict conforms to the expected format
        values = ['1', 'age_upon_outcome', 'animal_id', 'animal_type', 'breed', 'color', 'date_of_birth', 'datetime', 
          'monthyear', 'name', 'outcome_subtype', 'outcome_type', 'sex_upon_outcome', 'location_lat', 
          'location_long', 'age_upon_outcome_in_weeks']
        #loop to obtain input values from the user
        for i in range (len(values)):
            key = values[i]
            value = input("Enter " + values[i] + ": ")
            userCreateData.update({key: value})          #creates dict item with user input data
        #pprint(userCreateData)   <- old piece used for testing - kept for records/testing
        #print(type(userCreateData))  <- old piece used for testing - kept for records/testing
        
    #C operation for C in CRUD        
    def create(self, data):
        #use try/except block for boolean processing
        try:
            if data is not None:
                #print(type(data))  <- was used to confirm the data was a dictionary
                insert_result = self.database.animals.insert_one(data)     # data should be dictionary
                pprint(insert_result)
                #print("True")   <- old piece used for testing - kept for records/testing
                return True    #return value for boolean requirement
            
            else:
                # lets the user know something went wrong
                raise Exception("Nothing to save, because the data parameter is empty")
        except:
            #print("False")  <- old piece used for testing - kept for records/testing
            return False     #return value for boolean requirement
            
    #obtain target data for R in CRUD
    def obtainReadData(self):
        #loop to obtain a key/value pair
        for i in range(1):
            key = input("Enter search key: ")
            value = input("Enter search value: ")
            userSearchTarget.update({key: value})    #creates dict object to hold search terms
        #pprint(userSearchTarget) <- old piece used for testing - kept for records/testing
        #print(type(userSearchTarget)) <- old piece used for testing - kept for records/testing

    #R operation for R in CRUD
    def read(self, target):
        # try/except block for testing in the unit tests
        try:
            if target is not None:
                #print(type(target))       # target should be dictionary - confirmed
                read_result = list(self.database.animals.find(target, {"_id": False}))
                #pprint(read_result)   # displays the results in the console
                return read_result
            else:
                #lets the user know there was a problem
                raise Exception("Nothing to search, because the target parameter is empty")
                return False
        except Exception as e:
            print("An exception occurred: ", e)
    
    #obtain target data for U in CRUD
    def obtainUpdateData(self):
        #loop to obtain a key/value pair
        for i in range(1):
            key = input("Enter update key: ")
            value = input("Enter update value: ")
        userUpdateFromTarget.update({key: value})
        #obtain new data to change the target to
        for i in range(1):
            key = input("Enter update key: ")
            value = input("Enter new update value: ")
        userUpdateToTarget.update({'$set': {key: value}})
        print(userUpdateToTarget)

    #U operation for U in CRUD
    def update(self, fromTarget, toTarget, count):
        if fromTarget is not None:
            if count == 1:
                update_result = self.database.animals.update_one(fromTarget, toTarget)
                pprint("Matched Count: " + str(update_result.matched_count) + ", Modified Count: " + str(update_result.modified_count))
                if update_result.modified_count == 1:
                    print("Success!")
                    print(update_result)
                    return True
                else:
                    print("Something went wrong")
                    return False
            elif count == 2:
                update_result = self.database.animals.update_many(fromTarget, toTarget)
                pprint("Matched Count: " + str(update_result.matched_count) + ", Modified Count: " + str(update_result.modified_count))
                if update_result.modified_count == update_result.matched_count:
                    print("Success!")
                    print(update_result)
                    return True
                else:
                    print("Something went wrong, all items matching the target may not have been updated. Run a search to verify")
                    print(update_result)
                    return True
            else:
                print("Count not recognized - try again.")
                return False
        else:
            #lets the user know there was a problem
            raise Exception("Nothing to update, because at least one of the target parameters is empty")
            return False
    #obtain target data for D in CRUD
    def obtainDeleteData(self):
        #loop to obtain key/value pair
        for i in range(1):
            key = input("Enter delete key: ")
            value = input("Enter delete value: ")
            userDeleteTarget.update({key: value})
    #delete function for either single or many
    def deleteData(self, target, count):
        if target is not None:
            if count == 1:
                try:
                    delete_result = self.database.animals.delete_one(target)
                    pprint("Deleted Count: " + str(delete_result.deleted_count))
                    if delete_result.deleted_count == 0:
                        print("Nothing to be deleted using the target data.")
                        print(delete_result)
                        return True
                    else:
                        print("Success!")
                        print(delete_result)
                        return True
                except Exception as e:
                    print("An exception has occurred: ", e)
            elif count == 2:
                try:
                    delete_result = self.database.animals.delete_many(target)
                    pprint("Deleted Count: " + str(delete_result.deleted_count))
                    if delete_result.deleted_count == 0:
                        print("Nothing to be deleted using the target data.")
                        print(delete_result)
                        return True
                    else:
                        print("Success!")
                        print(delete_result)
                        return True
                except Exception as e:
                    print("An exception has occurred: ", e)
                    return False
            else:
                print("Count not recognized - try again.")
                return False
        else:
            #lets the user know there was a problem
            raise Exception("Nothing to delete, because the target parameter is empty")
            return False
            
# start the project in a loop for menu choices - not needed anymroe due to dashboar
#menuinput = 0
#user = input("Username: ")
#password = input("Password: ")
#if user enters anything other than 3, the loop repeats according to the rules below
#while (menuinput != 5):
#    secondaryinput = 0
#    try:
#        menuinput = int(input("Please Enter 1 to Create a Record, 2 to Search Records, 3 to Update a Record or Records, 4 to Delete a Record or Records, or 5 to Quit: "))
#    except Exception as e:
#        print("An exception occurred: ", e)
#        menuinput = 0
#    if menuinput == 1:
#        userShelter = AnimalShelter(user, password)
#        userShelter.obtainCreateData()
#        userShelter.create(userCreateData)
#        del(userShelter)
#    elif menuinput == 2:
#        userShelter = AnimalShelter(user, password)
#        userShelter.obtainReadData()
#        userShelter.read(userSearchTarget)
#        del(userShelter)
#    elif menuinput == 3:
#        userShelter = AnimalShelter(user, password)
#        secondaryinput = int(input("Enter 1 to update a single record or 2 to update multiple records: "))
#        userShelter.obtainUpdateData()
#        #update the target
#        userShelter.update(userUpdateFromTarget, userUpdateToTarget, secondaryinput)
#        del(userShelter)
#    elif menuinput == 4:
#        userShelter = AnimalShelter(user, password)
#        secondaryinput = int(input("Enter 1 to delete a single record or 2 to delete multiple records: "))
        #obtain the data to delete
#        userShelter.obtainDeleteData()
        #delete the data
#        userShelter.deleteData(userDeleteTarget, secondaryinput)
#        del(userShelter)
#    elif menuinput == 5:
#        break
#    else:
#        menuinput = 0
#        print("Invalid Entry, Please Try Again")
#Shelter1 = AnimalShelter() <- old piece used for testing - kept for records/testing
#Shelter1.obtainCreateData() <- old piece used for testing - kept for records/testing
#Shelter1.obtainReadData() <- old piece used for testing - kept for records/testing
        

# a sample data set for the create method that does work
sampleData = {
        '1': 3,
        'age_upon_outcome': '35 years',
        'animal_id': 'AAAA',
        'animal_type': 'Dogecoin',
        'breed': 'crypto',
        'color': 'green',
        'date_of_birth': 'wonder-years',
        'datetime': '2020-05-10 10:49:00',
        'monthyear': '2020-05-10T10:49:00',
        'name': 'monkeyboy',
        'outcome_subtype': 'SCRP',
        'outcome_type': 'super-transfer',
        'sex_upon_outcome': 'non-spayed',
        'location_lat': 30.6525984,
        'location_long': -97.74199,
        'age_upon_outcome_in_weeks': '450.454'
}
#a sample search term for read or delete (or the first part of update)
sampleTarget = {
    'animal_type': 'Dogecoin'
}
#a sample update element with 1 element
sampleUpdate = {'$set': {'name': '42'}}
#a sample update with multiple elements
sampleUpdateTwoField= { '$set': {
    'name': '42',
    'animal_type': 'Jaguar'}
}
#sample delete element
sampleDelete = {
    'name': 'Zz'
}