#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import telebot
import handlers as handlers

API_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(API_TOKEN)

commands = {
    'start': 'discover what\'s the purpose of Moobot',
    'help': 'list all Moobot available commands',
    'route': 'know the route to go to any place'
}

@bot.message_handler(commands=['start', 'help'])
def handleInfo(message):
    handlers.info_handler(bot, message)

@bot.message_handler(commands=['route'])
def handleRoute(message):
    handlers.process_handler(bot, message)

@bot.message_handler(commands=['prev', 'next'])
def handleStep(message):
    handlers.step_handle(bot, message)

bot.polling()
