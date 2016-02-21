#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import processManager as process_manager

bot_msg = json.load(open('messages.json'))

bot_commands = {
    'start': 'discover what\'s the purpose of Moobot',
    'help': 'list all Moobot available commands',
    'route': 'know the route to go to any place'
}

def get_bot_commands(prefix):
    cmds = ''
    for key, value in bot_commands.iteritems():
        cmds += '- Use /' + key + ' to ' + value + '\n'
    return prefix + cmds

def get_msg_command(text):
    return re.findall(r'/([a-zA-Z0-9]+)', text)[0]

def process_handler(bot, msg):
    cmdName = get_msg_command(msg.text)
    process_manager.execute(bot, cmdName)

def step_handler(bot):
    cmd = get_msg_command(msg.text)

    if cmd == 'prev':
        process_manager.prev_action(bot)
    elif cmd == 'next':
        process_manager.next_action(bot)

def info_handler(bot, msg):
    cmd = get_msg_command(msg.text)
    prefix = cmd == 'start' and 'start' or ''
    info_msg = get_bot_commands(prefix)

    bot.send_message(msg.chat.id, info_msg)
