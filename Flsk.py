#from flask import Flask # Импортируем модули
#app = Flask(__name__) # Создаем приложение

#@app.route("/") # Говорим Flask, что за этот адрес отвечает эта функция
#def hello_world():
#    return "It's working"
# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
import telegram

app = Flask(__name__)
app.debug = True

TOKEN = "891155181:AAH195_EE-NoWoBjDaI0Rrw3Fg5Ks_9xSBg"

global bot 
bot = telegram.Bot(token=TOKEN)

URL = '159.203.191.10' 

#WebHook
@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
    if request.method == "POST": 
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        try:
            kb = ReplyKeyboardMarkup([["Обновить"]])
            chat_id = update.message.chat.id 
            text = update.message.text
            userid = update.message.from_user.id
            username = update.message.from_user.username
            bot.send_message(chat_id=chat_id, text="hello", reply_markup=kb)
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

server_address = ("159.203.191.10", 27015)
server = valve.source.a2s.ServerQuerier(server_address)

def get_info():
    info = server.get_info()
    players = server.get_players()

    answer = "Players: {player_count}/{max_players} \nServer name: {server_name}\nGame: {game}\n".format(**info)
    for player in sorted(players["players"],
                         key=lambda p: p["score"], reverse=True):
        answer += "{name} {score} Dur: {duration}\n".format(**player)

    return answer
