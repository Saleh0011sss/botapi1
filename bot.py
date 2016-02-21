#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import telebot
import commands

def start(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'help'])
    def handle_info_command(message):
        commands.info(bot, message)

    @bot.message_handler(commands=['route'])
    def handle_route_command(message):
        commands.route(bot, message)

    @bot.message_handler(commands=['prev', 'next'])
    def handle_step_command(message):
        commands.step(bot, message)

    bot.polling()
