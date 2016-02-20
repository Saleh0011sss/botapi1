#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import run, post, get
import pymongo
from pymongo import MongoClient, ReturnDocument
from passlib.hash import pbkdf2_sha256
import lepl.apps.rfc3696
import random

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

# PUBLIC API METHODS

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
    if not isinstance(chatID, str):
        return None # not valid input type
    return db.users.find_one({ '_id' : chatID });

def doesUserExist(chatID):
    return isinstance(chatID, str) and db.users.find_one({ '_id' : chatID }) != None

def insertPayment(chatID, cardNumber, expDate, CVV):
    pass

print createUser('12031', 'jgferreiro.me@gmail.com', 1231, 696996)
print getUserByChat('12031')
print doesUserExist('12031')
