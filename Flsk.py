# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name, URL
import logging
from time import sleep

import telebot
import os
from flask import Flask, request

bot = telebot.TeleBot(bot_token)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route("/{}".format(bot_token), methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}/{}".format(URL,bot_token))
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))