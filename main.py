from config.config import *
from src.chat import predict_class, get_response, intents
import telebot
from flask import Flask, request
import time
from waitress import serve

#------------------------------------------------------------------------------

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

ints_prueba = predict_class("Hola") 
res_prueba = get_response(ints_prueba, intents) 
print(res_prueba)

# Gestión de mensajes
@bot.message_handler(content_types=['text'])
def bot_texto(message):
  ints = predict_class(message.text)
  res = get_response(ints, intents)
  bot.send_message(message.chat.id, res, parse_mode="html")


#main------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Configura el webhook
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(WEBHOOK_URL)
    # Inicia el servidor Flask
    serve(web_server, host="0.0.0.0", port = 5000)