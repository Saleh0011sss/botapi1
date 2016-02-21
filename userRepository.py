#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pymongo
from bottle import run, post, get
from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient, ReturnDocument

dbPath = 'localhost'
client = MongoClient(dbPath)
db = client['hackUPC']

"""
API METHODS:
- addUser(chatID, name, email, password, phone) :: True | False
- userExists(chatID) :: True | False
- getUserByChat(chatID) :: None | Dictionary

- addCard(chatID, cardNumber, expDate, CVC) :: True | False
- cardExist(chatID, cardNumber) :: True | False
- getCardsUser(chatID) :: None | Dictionary

- addPayment(chatID, creditNumber, text, price, qty, origen, destination) :: True | False
- paymentExist(chatID, cardNumber) :: True | False
- getPaymentsUser(chatID) :: None | Dictionary
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
Returns true if the user does not exist on our system
and True in the other case
"""
def userExists(chatID):
    return isTypeOf(chatID, 'String') and db.users.find_one({ '_id' : chatID }) != None


"""
Return False if the user exists or some parameters are not valid
and True if the user was inserted correctly.
"""
def addUser(chatID, name, email, password, phone):

    if userExists(chatID):
        return False

    user = {
        '_id' : str(chatID),
        'name' : str(name),
        'email' : str(email),
        'password' : encryptPass(str(password)),
        'phone' : str(phone),
        'cards' : [],
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
Returns true if the payment is already in our system
False if there is any payment with that number
"""
def cardExist(chatID, cardNumber):
    if not isTypeOf(cardNumber, 'String') or len(cardNumber) <= 0:
        return False
    return db.users.find_one({ '_id': chatID, 'cards._id' : cardNumber })

def paymentExist(chatID, cardNumber):
    if not isTypeOf(cardNumber, 'String') or len(cardNumber) <= 0:
        return False
    return db.users.find_one({ '_id': chatID, 'payments._id' : cardNumber })

"""
Given chatID, cardNumber, expDate and CVV we store it into the user.
Returns True if was successfully inserted
False in other cases (eg, duplicated card number)
"""
def addCard(chatID, cardNumber, expDate, CVC):

    user = getUserByChat(chatID)

    if user == None:
        return False # user does not exist

    if cardExist(chatID, cardNumber):
        return False # Card ID already on our system

    card = {
        '_id' : cardNumber,
        'expDate' : expDate,
        'CVC' : CVC
    }

    insertedCard = db.users.update({ '_id' : chatID }, {  '$push': { 'cards' : card }}, True);
    return True

def getCardsUser(chatID):
    user = getUserByChat(chatID)

    if user == None: return None
    return user['cards']

"""
Add one payment to the user
"""
def addPayment(chatID, creditNumber, text, price, qty, origen, destination):

    user = getUserByChat(chatID)
    
    if user == None:
        return False

    if paymentExist(chatID, creditNumber):
        return False # Card ID already on our system

    payment = {
        "_id" : creditNumber,
        "description" : text,
        "price" : price,
        "qty" : qty,
        "origin" : origen,
        "destination" : destination
    }

    insertedCard = db.users.update({ '_id' : chatID }, {  '$push': { 'payments' : payment }}, True);
    return True

def getPaymentsUser(chatID):
    user = getUserByChat(chatID)

    if user == None: return None
    return user['payments']


#### TESTS CASES

#userIDNum = "099"
# print "Created user ---- "
# print addUser(userIDNum, 'Raquel', 'lopez@hola.com', 1231, 696996)
# print "User ----"
# print getUserByChat(userIDNum)
# print "User exists----"
# print userExists(userIDNum)
# print "Add card----"
# print addCard(userIDNum, '12121212121', '12/20', '300')
# print "Cards----"
# print getCardsUser(userIDNum)
# print "Add Payment----"
#print addPayment(userIDNum, '121212212121', 'El puto mejor viaje', '23232', '2', '2', '3')
# print "Get paymens----"
# print getPaymentsUser(userIDNum)
