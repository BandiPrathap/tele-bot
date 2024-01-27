# Importa bibliotecas necesarias
import os
import random
import json
import pickle
import numpy as np
from tensorflow import keras
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Descargar recursos de NLTK
nltk.download('punkt') # Descarga de datos necesarios para la tokenización
nltk.download('wordnet')  # Descarga de datos para el lematizador
nltk.download('stopwords') # Descarga de datos para eliminación de stopwords
import h5py
from keras.models import load_model
import unicodedata

# Ruta de archivos utilizados por el chatbot
words_path = os.path.join('data','words.pkl')
classes_path = os.path.join('data','classes.pkl')
json_path = os.path.join('training_data','training.json')
model_path = os.path.join('models','chat_model.h5')

# Prepara el lematizador y carga los datos de entrenamiento
lematizer = WordNetLemmatizer()
intents = json.loads(open(json_path, encoding='utf-8').read())
words = pickle.load(open(words_path, 'rb'), encoding='latin1')
classes = pickle.load(open(classes_path, 'rb'), encoding='latin1')
# Cargar el modelo de aprendizaje automático
with h5py.File(model_path, 'r') as file:
    model = keras.models.load_model(file)

# Funciones para procesar y predecir basadas en la entrada del usuario
def clean_up_sentence(sentence):
    # Tokeniza y lematiza la oración, eliminando stopwords
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words if word not in set(stopwords.words('spanish'))]
    return sentence_words

# Convierte una oración en una bolsa de palabras
def bag_of_words(sentence):
    sentence = sentence.lower()  # Convierte el texto a minúsculas
    # Elimina tildes y normaliza
    sentence = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))
    # Eliminar tildes
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
     # Predice la clase de intención de una oración
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    minimum_probability = 0.8
    results = [[i, r] for i, r in enumerate(res) if r > minimum_probability]
    
    # Maneja la ausencia de predicciones con confianza alta
    if not results:
        return [{"intent": "desconocido", "probability": "1.0"}]

    results.sort(key = lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
    return return_list

# Obtiene una respuesta del chatbot basada en la intención predicha
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

# Pruebas del chat en consola (Mantener comentado si se hará un push en github)
"""
print("GO Bot is running!")
while True:
     message = input("")
     ints = predict_class(message)
     res = get_response(ints, intents)
     print(res)
"""