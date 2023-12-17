from config.config import *
import telebot
from flask import Flask, request
import time
from waitress import serve
import os
import random
import json
import pickle
import numpy as np
from tensorflow import keras
import nltk
from nltk.stem import WordNetLemmatizer
import h5py
from keras.models import load_model

# Ruta de archivos
words_path = os.path.join('data', 'words.pkl')
classes_path = os.path.join('data', 'classes.pkl')
json_path = os.path.join('training_data', 'training.json')
model_path = os.path.join('models','chat_model.h5')


lematizer = WordNetLemmatizer()
intents = json.loads(open(json_path, encoding='utf-8').read())
words = pickle.load(open(words_path, 'rb'), encoding='latin1')
classes = pickle.load(open(classes_path, 'rb'), encoding='latin1')
with h5py.File(model_path, 'r') as file:
    model = keras.models.load_model(file)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in  sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESOLD]

    results.sort(key = lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, training_json):
    tag = intents_list[0]['intent']
    list_of_intents = training_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

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

# Gestión de mensajes
@bot.message_handler(content_types=['text'])
def bot_texto(message):
  ints = predict_class(message.text)
  res = get_response(ints, intents)
  bot.send_message(message.chat.id, res, parse_mode="html")

#Gestión de mensajes
#@bot.message_handler(content_types = ['text'])
#def bot_texto(message):
#    bot.send_message(message.chat.id, message.text, parse_mode = "html")


#main------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Configura el webhook
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(WEBHOOK_URL)
    # Inicia el servidor Flask
    serve(web_server, host="0.0.0.0", port = 5000)