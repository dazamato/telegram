
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
            location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
            contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
            custom_keyboard = [[location_keyboard, contact_keyboard]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            bot.send_message(chat_id=chat_id,
                             text="Would you mind sharing your location and contact with me?",
                             reply_markup=reply_markup)

        except Exception as e:
            print(e)
    return 'ok'


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

