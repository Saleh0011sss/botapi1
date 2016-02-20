#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pymongo
import lepl.apps.rfc3696
from bottle import run, post, get
from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient, ReturnDocument

dbPath = 'localhost'
client = MongoClient(dbPath)
db = client['hackUPC']
emailValidator = lepl.apps.rfc3696.Email()

"""
API METHODS: 
- createUser(chatID, email, password, phone) :: True | False
- getUserByChat(chatID) :: None | Dictionary
- doesUserExist(chatID) :: True | False
"""

def encryptPass(password):
    rounds = random.randint(35000,60000) # random rounds
    salt_size = random.randint(800,900) # random salt size
    return pbkdf2_sha256.encrypt(password, rounds=rounds, salt_size=salt_size)

def validPassword(password, hash):
    try:
        return pbkdf2_sha256.verify(password, hash);
    except: # The password is not well formated (eg, using pbkd2_sha256 algorithm)
        return False

def isTypeOf(_elemn, typeStr):
    if typeStr == "String":
        return isinstance(_elemn, str)
    elif typeStr == "Number":
        return isinstance(_elemn, num)
    return False 

"""
Return False if the user exists or some parameters are not valid
and True if the user was inserted correctly.
"""
def createUser(chatID, email, password, phone):
    if not emailValidator(email):
        return False

    user = {
        '_id' : str(chatID),
        'email' : str(email),
        'password' : encryptPass(str(password)),
        'phone' : str(phone),
        'payments' : []
    }

    try:
        result = db.users.insert_one(user)
    except:
        return False # Problems inserting your username to our database

    return True

"""
Returns Dictionary if the user was found
and None in the rest of cases. 
"""
def getUserByChat(chatID):
    if not isTypeOf(chatID, 'String'):
        return None # not valid input type
    return db.users.find_one({ '_id' : chatID });

"""
Returns true if the user does not exist on our system
and True in the other case
"""
def doesUserExist(chatID):
    return isTypeOf(chatID, 'String') and db.users.find_one({ '_id' : chatID }) != None

"""
Given chatID, cardNumber, expDate and CVV we store it into the user.
Returns True if was successfully inserted
False in other cases (eg, duplicated card number)
"""
def insertPayment(chatID, cardNumber, expDate, CVV):
    pass

print "Created user: "
print createUser('122031', 'jgferreiro.me@gmail.com', 1231, 696996)

print "User chat: "
print getUserByChat('0012031')

print "Does user exist?: "
print doesUserExist('0012031')

print "Inserted Payment: "
print insertPayment('12031', '3949439439403', '12/20', '300')
