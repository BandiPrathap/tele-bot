import os
from dotenv import load_dotenv
#from config.config import *
from src.model.chat import predict_class, get_response, intents
from src.user.user_registration import is_user_registered, get_mail_from_user, register_user, unregister_user
from src.user.user_verification import verify_otp
from src.user.user_interactions import can_user_interact, get_interaction_count
from src.msg.msg import get_msg
from src.msg.menu import handle_menu
import telebot
from telebot import types
from flask import Flask, request
import time
from waitress import serve
import logging

load_dotenv('/config/.env')


logging.basicConfig(level= logging.INFO)

#------------------------------------------------------------------------------
#bot = telebot.TeleBot(TELEGRAM_TOKEN) #instancia del bot
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
otp_dict = {} #diccionario de estados
web_server = Flask(__name__) #intancia del servidor de Flask

#Gestiona las pesticones POST enviadas el servidor
@web_server.route('/', methods = ['POST'])
def web_hook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200

#comandos definidos para el bot bot 
commands = [
    types.BotCommand("start", "Iniciar el bot"),
    types.BotCommand("ayuda", "Obtener ayuda"),
    types.BotCommand("registrar", "Realizar el registro en el bot"),
    types.BotCommand("salir", "Cerrar sesión en el bot"),
    types.BotCommand("actividad", "Muestra el número de veces que has interactuado con el bot hoy")
]

bot.set_my_commands(commands)

"""Comando start"""
@bot.message_handler(commands = ["start"])
def cmd_start(message):
    bot.reply_to(message, get_msg('msg_start'))

"""Comando registrar"""
@bot.message_handler(commands=["registrar"])
def handle_registrar(message):
    chat_id = message.chat.id
    if not is_user_registered(chat_id):
        otp_dict[chat_id] = {"estado": "esperando_correo"}
        bot.send_message(chat_id, get_msg('msg_get_correo'))
    else:
        bot.send_message(chat_id, get_msg('msg_is_regitered'))

"""Comando salir"""
@bot.message_handler(commands=["salir"])
def handle_salir(message):
    chat_id = message.chat.id
    if is_user_registered(chat_id):
        otp_dict[chat_id] = {"estado": "esperando_correo_salir"}
        bot.send_message(chat_id, get_msg('msg_get_correo'))
    else:
        bot.send_message(chat_id, get_msg('msg_exit_is_not_regitered'))

@bot.message_handler(func=lambda message: message.chat.id in otp_dict and "correo" in otp_dict[message.chat.id]["estado"])
def handle_email_input(message):
    chat_id = message.chat.id
    estado = otp_dict[chat_id]["estado"]
    otp = get_mail_from_user(message, bot, estado)
    if otp:
        otp_dict[chat_id] = {"estado": "esperando_otp_salir" if estado == "esperando_correo_salir" else "esperando_otp", 
                             "otp": otp,
                             "correo": message.text}

# Agregar una lógica adicional para manejar el proceso de salida
@bot.message_handler(func=lambda message: message.chat.id in otp_dict and "otp" in otp_dict[message.chat.id]["estado"])
def handle_otp_input(message):
    chat_id = message.chat.id
    secret_info = otp_dict.get(chat_id)
    if secret_info:
        if secret_info["estado"] == "esperando_otp" and verify_otp(secret_info["otp"], message.text):
            del otp_dict[chat_id]  # Eliminar secreto ya utilizado
            register_user(secret_info["correo"], chat_id)
            bot.send_message(chat_id, get_msg('msg_ver_user'))
        elif secret_info["estado"] == "esperando_otp_salir" and verify_otp(secret_info["otp"], message.text):
            del otp_dict[chat_id]
            unregister_user(chat_id)
            bot.send_message(chat_id, get_msg('msg_exit_user'))
        else:
            bot.send_message(chat_id, get_msg('msg_wrong_otp'))
    else:
        pass


"""Comando ayuda"""
@bot.message_handler(commands = ["ayuda"])
def handle_help(message):
    bot.send_chat_action(message.chat.id, action = 'typing')
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    op1 = types.InlineKeyboardButton('¿Cómo registrarme al bot?', callback_data='registro')
    op2 = types.InlineKeyboardButton('¿Cómo darme de baja del bot?', callback_data='baja')
    op3 = types.InlineKeyboardButton('Más acerca del bot', callback_data='acerca_de')
    op4 = types.InlineKeyboardButton('Enlaces de interés', callback_data='links')
    op5 = types.InlineKeyboardButton('¿Cuántas veces he usado el chat?', callback_data='actividad')
    
    markup.add(op1, op2, op3, op4, op5)
    bot.send_message(message.chat.id, '¿En qué necesitas ayuda?', reply_markup = markup)


@bot.callback_query_handler(func=lambda call: True)
def menu_answer(callback_query):
    handle_menu(bot, callback_query)  # Utiliza la función del archivo menu.py

"""Comando actividad"""
@bot.message_handler(commands=["actividad"])
def handle_actividad(message):
    chat_id = message.chat.id
    if is_user_registered(chat_id):
        num_interacciones = get_interaction_count(chat_id)
        bot.send_message(chat_id, f"Haz interactuado con el bot {num_interacciones} veces hoy.")
    else:
        bot.send_message(chat_id, "Necesitas estar registrado para usar este comando.")


"""Mensajes del bot"""
@bot.message_handler(content_types=["text"])
def resp_mensajes(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, action = 'typing')
    if chat_id in otp_dict:
        # Manejo del OTP si el usuario está en el proceso de registro
        handle_otp_input(message)
    elif not is_user_registered(chat_id):
        bot.send_message(chat_id, get_msg('msg_user_is_not_registered'))
    elif not can_user_interact(chat_id):
        bot.send_message(chat_id,  get_msg('msg_limit')) 
    else:
        ints = predict_class(message.text)
        res = get_response(ints, intents)
        bot.send_message(message.chat.id, res, parse_mode="html")

#main------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Configura el webhook
    bot.remove_webhook()
    time.sleep(1)
    #bot.set_webhook(WEBHOOK_URL)
    bot.set_webhook(os.getenv('WEBHOOK_URL'))
    # Inicia el servidor Flask
    serve(web_server, host="0.0.0.0", port = 5000)
