#!/usr/bin/env python
# -*- coding: utf-8 -*-

currentStep = 0
process_name = 'route'
process_list = json.load(open('processes.json'))
process_list = process_list[cmd]

def checkLimits():
    return

def execute(bot, processName):
    if currentStep >= len(process_list):
        return

    if (process_list == None)
        process_list = json.load(open('processes.json'))

    bot.send(process_list[currentStep])
    currentStep += 1 
    execute(bot, process_list)

def prev_action():
    if currentStep <= 0:
        return
    currentStep -= 1

def next_action():
    if inserted < currentStep:
        return
    currentStep += 1

# process_steps = {
#        'route': [
#          {
#            "alert" : "typing || u",
#            "text": "",
#            "type": "printAction || promptAction",
#            "validation" : "Mail, Name, City, Message"
#          },
#         ]
#       }
#
# {
#
#     'process_steps': [
#         {
#             ['send_message', [1,2]]
#
#         bot[action., process_steps[1]]
#         bot[process_steps[0], process_steps[1]]
#         bot[process_steps[0], process_steps[1]]
#             ['send_message', [1,2]]
#         }
#     ]
# }
