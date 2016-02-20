import re

bot_msg = json.load(open('messages.json'))
process_list = json.load(open('messages.json'))

bot_commands = {
    'start': 'discover what\'s the purpose of Moobot',
    'help': 'list all Moobot available commands',
    'route': 'know the route to go to any place'
}

def get_bot_commands(prefix):
    cmds = ''
    for key, value in commands.iteritems():
        cmds += '- Use /' + key + ' to ' + value + '\n'
    return prefix + cmds

def get_msg_command(msg):
    cmd_re = re.compile('/([a-zA-Z0-9]+)')
    return command_re.findall(msg)

def process_handler(msg):
    cmd = get_msg_command(msg)

    process = process_list(cmd)
    process_manager.execute(process)

def step_handler(msg):
    cmd = get_msg_command(msg)

    if cmd == 'prev':
        process_manager.prev_action()
    elif cmd == 'next':
        process_manager.next_action()

def info_handler(msg):
    cmd = get_msg_command(msg)
    prefix = cmd == 'start' and 'start' or ''
    info_msg = get_bot_commands(prefix)

    bot.send_message(msg.chat.id, info_msg)
