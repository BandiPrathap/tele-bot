from config.config import *
import telebot
from flask import Flask, request
import time
from waitress import serve

#instancia del bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#intancia del servidor de Flask
web_server = Flask(__name__)

#Gestiona las pesticones POST enviadas el servidor
@web_server.route('/', methods = ['POST'])
def web_hook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200

#Comando start
@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Hola", parse_mode = "html")

#Gestión de mensajes
@bot.message_handler(content_types = ['text'])
def bot_texto(message):
    bot.send_message(message.chat.id, message.text, parse_mode = "html")

#main------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Configura el webhook
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(WEBHOOK_URL)

    # Inicia el servidor Flask
    serve(web_server, host="0.0.0.0", port = 5000)