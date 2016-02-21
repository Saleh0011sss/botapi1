# -*- coding: utf-8 -*-
import sys
#sys.path.append('./userRepository')
import userRepository as database
import lepl.apps.rfc3696

emailValidator = lepl.apps.rfc3696.Email()

"""
API METHODS:
- createUser(chatID, name, email, password, phone) :: True || False
- userExists(chatID) :: True || False
- getUserByChat() :: User Object - None

- addCard(chatID, cardNumber, expDate, CVC) :: True || False
- addPayment(chatID, creditNumber, text, price, qty, origen, destination) || True | False
"""

def empty(data):
    return len(str(data)) <= 0

def userExists(chatID):
    return database.userExists(chatID)

def createUser(chatID, name, email, password, phone):
    if empty(chatID) or empty(name) or empty(email) or empty(chatID) or empty(password) or not emailValidator(email):
        return False # Validation fails

    return database.addUser(chatID, name, email, password, phone)

""" Returns None if user doesnt exist.
    And the object if the user exists. """
def getUserByChat(chatID):
    return database.getUserByChat(chatID)

def addCard(chatID, cardNumber, expDate, CVC):

    if empty(chatID) or empty(cardNumber) or empty(expDate) or empty(CVC):
        return False # Validation fails

    return database.addCard(chatID, cardNumber, expDate, CVC)

def addPayment(chatID, creditNumber, text, price, qty, origen, destination):
    # TODO: Add checks here :)
    return database.addPayment(chatID, creditNumber, text, price, qty, origen, destination)

# print createUser('111111111', 'Paco', 'paco@paco.com', '123', '121')
# print addPayment('111111111', '39422943294394030', '12/20', '300', '1', '23,30', '23,30')
