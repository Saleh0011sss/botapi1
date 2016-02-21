import re

def get_command_name(text):
    return re.findall(r'/([a-zA-Z0-9]+)', text)[0]
