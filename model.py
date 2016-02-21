# -*- coding: utf-8 -*-
import sys
#sys.path.append('./userRepository')
import userRepository as database
import lepl.apps.rfc3696

emailValidator = lepl.apps.rfc3696.Email()

"""
API METHODS:
- checkUser(chatID) :: True || False
- createUser(chatID, name, email, password, phone) :: True || False
- addPayment(chatID, cardNumber, expDate, CVC) :: True || False
- getUser() :: User Object - None
"""

def empty(data):
    return len(str(data)) <= 0

def checkUser(chatID):
    return userExists(chatID)


def createUser(chatID, name, email, password, phone):
    if empty(chatID) or empty(name) or empty(email) or empty(chatID) or empty(password) or not emailValidator(email):
        return False # Validation fails

    return database.createUser(chatID, name, email, password, phone)

def addPayment(chatID, cardNumber, expDate, CVC):

    if empty(chatID) or empty(cardNumber) or empty(expDate) or empty(CVC):
        return False # Validation fails

    return database.addPayment(chatID, cardNumber, expDate, CVC)

""" Returns None if user doesnt exist.
    And the object if the user exists. """
def getUser(chatID):
    return database.getUserByChat(chatID)
