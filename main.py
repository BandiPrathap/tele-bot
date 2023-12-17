from config.config import *
import os
import json
from src.chat import predict_class, get_response
import telebot
from flask import Flask, request
import time
from waitress import serve

#instancia del bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#intancia del servidor de Flask
web_server = Flask(__name__)

# Cargar el modelo y datos del chat
json_path = os.path.join('training_data', 'training.json')
intents = json.loads(open(json_path, encoding='utf-8').read())

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
#@bot.message_handler(content_types = ['text'])
#def bot_texto(message):
#    bot.send_message(message.chat.id, message.text, parse_mode = "html")

# Gestión de mensajes
@bot.message_handler(content_types=['text'])
def bot_texto(message):
    # Obtener la respuesta del chat
    response = get_chat_response(message.text)
    # Enviar la respuesta al usuario
    bot.send_message(message.chat.id, response)

def get_chat_response(message):
    # Obtener la respuesta del modelo de chat
    intents_list = predict_class(message)
    response = get_response(intents_list, intents)
    print("Chat Response:", response) 
    return response

#main------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Configura el webhook
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(WEBHOOK_URL)
    print(WEBHOOK_URL)
    # Inicia el servidor Flask
    serve(web_server, host="0.0.0.0", port = 5000)