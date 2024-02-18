from telebot import TeleBot
from src.msg.msg import get_msg

def registro_callback(bot: TeleBot, callback_query):
    bot.send_message(callback_query.message.chat.id, get_msg(msg_name='msg_help_login'))

def baja_callback(bot: TeleBot, callback_query):
    bot.send_message(callback_query.message.chat.id, get_msg(msg_name='msg_help_logout'))

def acerca_de_callback(bot: TeleBot, callback_query):
    bot.send_message(callback_query.message.chat.id, get_msg(msg_name='msg_about'))

def links_callbak(bot: TeleBot, callback_query):
    bot.send_message(callback_query.message.chat.id, get_msg(msg_name='msg_links'))
    
def actividad_callback(bot: TeleBot, callback_query):
    bot.send_message(callback_query.message.chat.id, get_msg(msg_name='msg_help_actividad'))

def handle_menu(bot: TeleBot, callback_query):
    callback_handlers = {
        'registro': registro_callback,
        'baja': baja_callback,
        'acerca_de': acerca_de_callback,
        'links': links_callbak,
        'actividad': actividad_callback
    }

    handler = callback_handlers.get(callback_query.data)
    if handler:
        handler(bot, callback_query)
    else:
        bot.send_message(callback_query.message.chat.id, 'Opción no reconocida')