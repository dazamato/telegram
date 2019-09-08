# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name, URL
import logging
from time import sleep

app = Flask(__name__)
app.debug = True

TOKEN = bot_token

global bot 
bot = telegram.Bot(token=TOKEN)


#WebHook
@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
    if request.method == "POST": 
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        try:
            chat_id = update.message.chat.id 
            text = update.message.text
            userid = update.message.from_user.id
            username = update.message.from_user.username
            bot.send_message(chat_id=chat_id, text="hello")
        except Exception as e:
            print (e)
    return 'ok' 

#Set_webhook 
@app.route('/set_webhook', methods=['GET', 'POST']) 
def set_webhook(): 
    s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/server.crt', 'rb')) 
    if s:
        print(s)
        return "webhook setup ok" 
    else: 
        return "webhook setup failed" 

@app.route('/') 
def index(): 
    return '<h1>Hello</h1>'




try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2


def main():
    # Telegram Bot Authorization Token
    bot = telegram.Bot(TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            update_id = echo(bot, update_id)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            elif e.message == "Unauthorized":
                # The user has removed or blocked the bot.
                update_id += 1
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            sleep(1)


def echo(bot, update_id):

    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
        message = update.message.text

        if message:
            # Reply to the message
            bot.sendMessage(chat_id=chat_id,
                            text=message)

    return update_id


if __name__ == '__main__':
    main()