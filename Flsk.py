
from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name,URL
from mastermind import get_response


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

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
            print(e)
    return 'ok'
# @app.route('/{}'.format(TOKEN), methods=['POST'])
# def respond():
#     # retrieve the message in JSON and then transform it to Telegram object
#     update = telegram.Update.de_json(request.get_json(force=True), bot)
#
#     chat_id = update.message.chat.id
#     msg_id = update.message.message_id
#
#     # Telegram understands UTF-8, so encode text for unicode compatibility
#     text = update.message.text.encode('utf-8').decode()
#     print("got text message :", text)
#
#     response = get_response(text)
#     bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
#
#     return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/dazamato-tele/server.crt', 'rb'))
    if s:
        print(s)
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '<h1>Hello_!!</h1>'


if __name__ == '__main__':
    app.run(threaded=True)