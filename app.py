import os
import json
import telebot

API_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(API_TOKEN)

commands = {
    'start': 'Get used to the bot',
    'help': 'Gives you information about how to interact with Transport Bot'
}

with open('messages.json') as messages_file:
    messages = json.load(messages_file)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, messages['welcome'])

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, messages['help'])

@bot.message_handler(commands=['route'])
def start_route_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, messages['route']['start'])
    bot.register_next_step_handler(message, validate_address_input)

def validate_address_input(message):
    address = message.text
    bot.send_message(message.chat.id, 'Your address is ' + message.text + '. Type \'change\' to change your answer')
    bot.register_next_step_handler(message, check_if_back)

def check_if_back(message):
    response = message.text
    if response == 'change':
        change_param(message)

def change_param(message):
    bot.send_message(message.chat.id, 'Well, introduce a new address')
    bot.register_next_step_handler(message, validate_address_input)

bot.polling()
