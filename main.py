import os
import bot

API_TOKEN = os.environ['TELEGRAM_TOKEN']

bot.start(API_TOKEN)
