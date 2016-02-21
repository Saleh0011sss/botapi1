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

def print_action(bot, msg, process_name, start_index, action):
    bot.send_chat_action(msg.chat.id, action['alert'])
    bot.send_message(msg.chat.id, action['content'])
    execute_action(bot, msg, process_name, start_index + 1)

def prompt_action(bot, msg, process_name, start_index, action):

    def validate(msg):
        if msg.text == 'Alex':
            execute_action(bot, msg, process_name, start_index + 1)
        else:
            prompt_action(bot, msg, process_name, start_index, action)

    bot.send_chat_action(msg.chat.id, action['alert'])
    bot.send_message(msg.chat.id, 'who\'s the best')
    bot.register_next_step_handler(msg, validate)


def execute_action(bot, msg, process_name, start_index):
    if start_index >= len(process_list[process_name]) - 1:
        return

    process_actions = process_list[process_name]

    action = process_actions[start_index]
    if action['type'] == 'print':
        print_action(bot, msg, process_name, start_index, action)
    if action['type'] == 'prompt':
        prompt_action(bot, msg, process_name, start_index, action)

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
