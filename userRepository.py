#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import run, post, get
import pymongo
from pymongo import MongoClient, ReturnDocument

dbPath = 'localhost'
client = MongoClient(dbPath)
db = client['hackUPC']

class User:
    __init__(self, chatID, email, password, phone=''):
        self.chatID = chatID
        self.email = email
        self.password = password
        self.phone = phone

@get('/user/<chatID>')
def getUserByChatID(chatID):
    print "Hola"
    print chatID

run(host='localhost', port=8080);