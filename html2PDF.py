# -*- coding: utf-8 -*-
import os
import json
import telebot
import pdfcrowd
import urllib
import re

API_TOKEN = os.environ['TELEGRAM_TOKEN']
#PDFCROWD_USERNAME = os.environ['PDFCROWD_USERNAME']
#PDFCROWD_KEY = os.environ['PDFCROWD_USERNAME']

PDFCROWD_USERNAME = "joralex"
PDFCROWD_KEY = "218015675372493d0b8b8bc01fe8d0ea"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['receipt'])
def generate_receipt(message):

    print message
    chat_id = message.chat.id
    username = message.chat.username
    firstName = message.chat.first_name
    print firstName

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
        bot.send_message(chat_id, 'Sorry! I fail this time. We\'re goint to write you an email with the recepeit')
        print('Failed: {}'.format(why))


@bot.message_handler(commands=['document'])
def send_travel(message):

    print message

    chat_id = message.chat.id

    name = message.chat.first_name
    html = "<h1>Thank you," + name + "</h1>"
    html += "<p>You have just bought your ticket</p>"
    html += "<p>Hope you enjoy your travel</p>"
    html += "<p>Best,<br/></p>"

    _input = os.path.dirname(os.path.realpath(__file__)) + '/file1.html'
    output = os.path.dirname(os.path.realpath(__file__)) + '/hola.pdf'

    try:

        bot.send_message(chat_id, 'I\'m genereting your recepit. Please be patient ;)')

        # create an API client instance
        client = pdfcrowd.Client(PDFCROWD_USERNAME, PDFCROWD_KEY)

        # convert a web page and store the generated PDF into a pdf variable
        #pdf = client.convertURI('http://www.google.com')

        # convert an HTML string and save the result to a file
        output_file = open('html.pdf', 'wb')

        name = message.chat.first_name
        html = "<h1>Thank you," + name + "</h1>"
        html += "<p>You have just bought your ticket</p>"
        html += "<p>Hope you enjoy your travel</p>"
        html += "<p>Best,<br/></p>"
        client.convertHtml(html, output_file)
        output_file.close()

        #f = open('tarjeta.png', 'rb')  # some file on local disk
        f = open('html.pdf', 'rb')  # some file on local disk
        response = bot.send_document(chat_id, f)
        #pprint(response)


        # convert an HTML file
        #output_file = open('file.pdf', 'wb')
        #client.convertFile('/path/to/MyLayout.html', output_file)
        #output_file.close()

    except pdfcrowd.Error, why:
        bot.send_message(chat_id, 'Sorry! I fail this time. We\'re goint to write you an email with the recepeit')
        print('Failed: {}'.format(why))


bot.polling()
