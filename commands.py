#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import utils

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

def print_action(bot, msg, action):
    bot.send_chat_action(msg.chat.id, action['alert'])
    bot.send_message(msg.chat.id, action['content'])

def prompt_action(bot, msg, action):
    def create_validate_fn(msg):
        if msg.text == 'Alex':
            bot.send_chat_action(msg.chat.id, action['alert'])
            bot.send_message(msg.chat.id, action['msg'])
        else:
            prompt_action(bot, msg, action)

    bot.send_chat_action(msg.chat.id, action['alert'])
    bot.send_message(msg.chat.id, 'who\'s the best')
    bot.register_next_step_handler(msg, create_next_step_handler)


def execute_action(bot, msg, process_name, start_index):

    process_actions = process_list[process_name]

    action = process_actions[start_index]
    if action['type'] == 'print':
        print_action(bot, msg, action)
    if action['type'] == 'prompt':
        prompt_action(bot, msg, action)

    next_index = start_index + 1
    if next_index <= len(process_actions) - 1:
        execute_action(bot, msg.chat.id, process_name, start_index + 1)

# def prev_action():
#     if currentStep <= 0:
#         return
#     currentStep -= 1
#
# def next_action():
#     if inserted < currentStep:
#         return
#     currentStep += 1

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

# def step(bot):
#     cmd = utils.get_command_name(msg.text)
#
#     if cmd == 'prev':
#         process_manager.prev_action(bot)
#     elif cmd == 'next':
#         process_manager.next_action(bot)
