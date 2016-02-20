import os
import json
import telebot

API_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(API_TOKEN)

with open('messages.json') as messages_file:
    messages = json.load(messages_file)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages['welcome'])

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, messages['help'])

bot.polling()
