import os
import random
import json
import pickle
import numpy as np
from tensorflow import keras
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import h5py
from keras.models import load_model

#------------------------------------------------------------------------------------------
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
    sentence = sentence.lower()  # Convierte el texto a minúsculas
    sentence = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))  # Eliminar tildes
    sentence_words = nltk.word_tokenize(sentence)
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
    ERROR_THRESOLD = 0.7
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESOLD]

    # Verifica si hay alguna predicción con suficiente confianza
    if not results:
        return [{"intent": "desconocido", "probability": "1.0"}]

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
        elif tag == "desconocido":
            result = "No he entendido tu pregunta, sé más específico"
            break
    return result
