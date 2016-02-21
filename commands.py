#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import utils
import model
import re
import pdfcrowd
import urllib
import os

user = {
    'chatID': '',
    'name': '',
    'email': '',
    'password': '',
    'phone': ''
}
action_index = 0
# process_list = process_list[cmd]
# process_name = 'route'
process_list = json.load(open('commands.json'))
bot_msg = json.load(open('messages.json'))
bot_commands = {
    'start': 'discover what\'s the purpose of Moobot',
    'help': 'list all Moobot available commands',
    'route': 'know the route to go to any place'
}

API_TOKEN = os.environ['TELEGRAM_TOKEN']
#PDFCROWD_USERNAME = os.environ['PDFCROWD_USERNAME']
#PDFCROWD_KEY = os.environ['PDFCROWD_USERNAME']

PDFCROWD_USERNAME = "joralex"
PDFCROWD_KEY = "218015675372493d0b8b8bc01fe8d0ea"

def receipt_action(bot, msg, process_name, start_index, action):

    chat_id = msg.chat.id
    username = msg.chat.username
    firstName = msg.chat.first_name

    filename = '-' + firstName + '_' + username + '_bill.pdf'

    input_html = os.path.dirname(os.path.realpath(__file__)) + '/static/bill.html'
    output_pdf = os.path.dirname(os.path.realpath(__file__)) + filename

    try:
        bot.send_chat_action(chat_id, 'typing')
        bot.send_message(chat_id, 'I\'m genereting your recepit. Please be patient ;)')
        client = pdfcrowd.Client(PDFCROWD_USERNAME, PDFCROWD_KEY) # create an API client instance

        # Get a file-like object for the Python Web site's home page.
        f = urllib.urlopen(input_html)
        # Read from the object, storing the page's contents in 's'.
        htmlPage = f.read()
        f.close()

        service = 'Travel from madrid to Barcelona'
        price = 30
        quantity = 3
        total = price * quantity

        htmlPage = htmlPage % (service, price, quantity, total, total)

        output_file = open(output_pdf, 'wb')
        client.convertHtml(htmlPage, output_file)
        output_file.close()

        f = open(output_pdf, 'rb')  # some file on local disk
        response = bot.send_document(chat_id, f)
        f.close()

    except pdfcrowd.Error, why:
        bot.send_message(chat_id, 'Sorry! I fail this time. We\'re goint to write you an email with the recepeit. Promise 🙌🏻')
        print('Failed: {}'.format(why))


def print_action(bot, msg, process_name, start_index, action):
    if 'params' in action:
        content_params = action['params'] and action['params'] or []
        if len(content_params) == 1:
            action['content'].format(unicode(user[content_params[0]],'utf-8'), unicode(user[content_params[0]],'utf-8'), unicode(user[content_params[0]],'utf-8'))
        elif len(content_params) == 2:
            action['content'].format(unicode(user[content_params[0]],'utf-8'), unicode(user[content_params[0]],'utf-8'))
        elif len(content_params) == 3:
            action['content'].format(unicode(user[content_params[0]],'utf-8'))

    bot.send_chat_action(msg.chat.id, action['alert'])
    bot.send_message(msg.chat.id, action['content'])
    execute_action(bot, msg, process_name, start_index + 1)

def prompt_action(bot, msg, process_name, start_index, action):

    def validate_prompt(msg):
        if msg.text != '':
            user[action['field']] = msg.text
            execute_action(bot, msg, process_name, start_index + 1)
        else:
            prompt_action(bot, msg, process_name, start_index, action)

    bot.send_chat_action(msg.chat.id, action['alert'])

    bot.send_message(msg.chat.id, action['content'])
    bot.register_next_step_handler(msg, validate_prompt)

def selector_action(bot, msg, process_name, start_index, action):
    params = action["params"]

    def validate_prompt(msg):
        if msg.text != '':
            user[action['field']] = msg.text
            execute_action(bot, msg, process_name, start_index + 1)
        else:
            prompt_action(bot, msg, process_name, start_index, action)

    bot.send_chat_action(msg.chat.id, action['alert'])
    bot.send_message(msg.chat.id, action['content'])

    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(params[0], params[1], params[2])
    bot.send_message(msg.chat.id, action['content'], reply_markup=markup)
    bot.register_next_step_handler(msg, validate_prompt)

def location_action(bot, msg, process_name, start_index, action):

    def validate_location(msg):
        if msg.text == 'yes':
            print "foo"
            execute_action(bot, msg, process_name, start_index + 1)
        else:
            location_action(bot, msg, process_name, start_index, action)

    bot.send_chat_action(msg.chat.id, action['alert'])

    bot.send_message(msg.chat.id, action['content'])

    bot.send_chat_action(msg.chat.id, 'find_location')
    bot.send_location(msg.chat.id, '41.382819', '2.116023')

    bot.register_next_step_handler(msg, validate_location)

def selector_action(bot, msg, process_name, start_index, action):

    def validate_location(msg):
        if msg.text == 'yes':
            print "foo"
            execute_action(bot, msg, process_name, start_index + 1)
        else:
            location_action(bot, msg, process_name, start_index, action)

    bot.send_chat_action(msg.chat.id, action['alert'])

    bot.send_message(msg.chat.id, action['content'])

    bot.send_chat_action(msg.chat.id, 'find_location')
    bot.send_location(msg.chat.id, '41.382819', '2.116023')

    bot.register_next_step_handler(msg, validate_location)


def execute_action(bot, msg, process_name, start_index):
    if start_index == 0:
        user['chatID'] = msg.chat.id
        user['password'] = '111111'

    print "bar"
    print start_index
    if start_index > len(process_list[process_name]) - 1:
        return

    if start_index == len(process_list[process_name]) - 1:

        print user['chatID']
        print model.getUserByChat(user['chatID'])

        # print user
        inserted = model.createUser(
            user['chatID'],
            user['name'],
            user['email'],
            user['password'],
            user['phone']
        )

        #if inserted / NEW USER
        # ELSE / OLD USER

        print model.getUserByChat(123123123)

    process_actions = process_list[process_name]

    action = process_actions[start_index]
    if action['type'] == 'print':
        print_action(bot, msg, process_name, start_index, action)
    if action['type'] == 'prompt':
        prompt_action(bot, msg, process_name, start_index, action)
    if action['type'] == 'receipt':
        receipt_action(bot, msg, process_name, start_index, action)
    if action['type'] == 'location':
        location_action(bot, msg, process_name, start_index, action)

def info(bot, msg):
    cmd_name = utils.get_command_name(msg.text)
    prefix = cmd_name == 'start' and bot_msg['start'] or ''

    command_list = ''
    for key, value in bot_commands.iteritems():
        command_list += '- Use /' + key + ' to ' + value + '\n'

    bot.send_message(msg.chat.id, prefix + command_list)

def route(bot, msg):
    cmd_name = utils.get_command_name(msg.text)
    execute_action(bot, msg, cmd_name, 0)

# def prev_action():
#     if currentStep <= 0:
#         return
#     currentStep -= 1
#
# def next_action():
#     if inserted < currentStep:
#         return
#     currentStep += 1

# def step(bot):
#     cmd = utils.get_command_name(msg.text)
#
#     if cmd == 'prev':
#         process_manager.prev_action(bot)
#     elif cmd == 'next':
#         process_manager.next_action(bot)
