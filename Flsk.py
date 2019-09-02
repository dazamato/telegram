from flask import Flask # Импортируем модули
app = Flask(__name__) # Создаем приложение

@app.route("/") # Говорим Flask, что за этот адрес отвечает эта функция
def hello_world():
    return "It's working"