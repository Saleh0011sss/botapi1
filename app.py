import os
import json
import telebot
import handlers

API_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(API_TOKEN)

commands = {
    'start': 'discover what\'s the purpose of Moobot',
    'help': 'list all Moobot available commands',
    'route': 'know the route to go to any place'
}

@bot.message_handler(commands=['start', 'help'])
handlers.info_handler(message)

@bot.message_handler(commands=['route'])
handlers.process_handler(message)

@bot.message_handler(commands=['prev', 'next'])
handlers.step_handler(message)

bot.polling()
