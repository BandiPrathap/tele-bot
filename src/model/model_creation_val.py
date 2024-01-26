# Importaciones de bibliotecas necesarias
import os
import random
import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.regularizers import l2
import nltk
nltk.download('punkt') # Descarga de datos necesarios para la tokenización
nltk.download('wordnet')  # Descarga de datos para el lematizador
from nltk.stem import WordNetLemmatizer
import unicodedata
from sklearn.model_selection import StratifiedKFold
from collections import defaultdict

# Rutas para guardar y cargar archivos como listas de palabras, clases, datos de entrenamiento y modelo
words_path = os.path.join('data','words.pkl')
classes_path = os.path.join('data','classes.pkl')
json_path = os.path.join('training_data','training.json')
model_path = os.path.join('models','chat_model.h5')
# Carga de los datos de entrenamiento desde 'training.json'
with open(json_path, 'r', encoding='utf-8') as json_file:
    intents = json.load(json_file)

# Elimina tildes del texto
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Inicializa el lematizador
lemmatizer = WordNetLemmatizer()

# Inicializa listas y variables para procesar las palabras y clases
words = [] # Almacena todas las palabras
classes = [] # Almacena todas las clases
documents = [] # Almacena las palabras con su respectivo identificador o clase
ignoreLetters = ['¿','?','¡','!','.',',',';'] # Caracteres a ignorar

# Recorre los datos del json para rellenar las listas
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokeniza el patrón en palabras
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList) # Agrega las palabras a la lista 'words'
        documents.append((wordList, intent['tag'])) # Agrega las palabras y su clase a 'documents'
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lematizando, filtrando las palabras y quitando tildes para ordenarlas y eliminar duplicados
words = [lemmatizer.lemmatize(remove_accents(word).lower()) for word in words if word not in ignoreLetters]
words = sorted(set(words))
classes = sorted(set(classes))

# Guardando las listas de palabras y clases en archivos binarios
pickle.dump(words, open(words_path, 'wb'))
pickle.dump(classes, open(classes_path, 'wb'))

# Preparando los datos de entrenamiento
training = []
outputEmpty = [0] * len(classes)

# Para cada documento, se crea un bag de palabras binarias y la etiqueta correspondiente
for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    # Crea un bag de palabras binarias
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)
    # Crea una lista de salida categórica
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    # Combina el bag de palabras con la lista de salida y se agregan a la lista 'training'
    training.append(bag + outputRow)

# Mezclan aleatoriamente los datos de entrenamiento
random.shuffle(training)
# Convierte 'training' a una matriz NumPy
training = np.array(training)

# Divide 'training' en matrices de entrada ('trainX') y salida ('trainY')
trainX = training[:, :len(words)]
trainY = training[:, len(words):]

# Agrupa los documentos por tag
grouped_documents = {}
for document in documents:
    tag = document[1]
    if tag not in grouped_documents:
        grouped_documents[tag] = []
    grouped_documents[tag].append(document)

# Divide cada grupo en 'K' partes
num_folds = 5
for i, item in enumerate(grouped_documents[tag]):
    print(f"Element {i}: length {len(item)}, type {type(item)}")
grouped_folds = {tag: np.array_split(grouped_documents[tag], num_folds) for tag in grouped_documents}


# Construye los folds para la validación cruzada
folds = []
for i in range(num_folds):
    fold_documents = []
    for tag in grouped_folds:
        fold_documents.extend(grouped_folds[tag][i])
    folds.append(fold_documents)

# Asegura que cada fold tenga al menos un ejemplo de cada intent
def distribute_documents_evenly(grouped_documents, num_folds):
    folds = [[] for _ in range(num_folds)]
    for tag, docs in grouped_documents.items():
        split_docs = np.array_split(docs, num_folds) if len(docs) >= num_folds else [docs] * num_folds
        for i, fold_docs in enumerate(split_docs):
            folds[i].extend(fold_docs)
    return folds

# Distribuye los documentos entre los folds
folds = distribute_documents_evenly(grouped_documents, num_folds)

# Convierte los folds en formato adecuado para entrenamiento y prueba
fold_data = []
for fold in folds:
    training = []
    for document in fold:
        bag = [1 if word in document[0] else 0 for word in words]
        output_row = [0] * len(classes)
        output_row[classes.index(document[1])] = 1
        training.append(bag + output_row)
    training = np.array(training)
    fold_data.append((training[:, :len(words)], training[:, len(words):]))

# Inicializa las métricas de rendimiento
acc_per_fold = []
loss_per_fold = []

# Validación Cruzada
for fold_no in range(num_folds):
    # Prepara los datos de entrenamiento y prueba para la iteración actual
    train_data = [data for i, data in enumerate(fold_data) if i != fold_no]
    test_data = fold_data[fold_no]

    trainX = np.vstack([data[0] for data in train_data])
    trainY = np.vstack([data[1] for data in train_data])
    testX, testY = test_data

    #creación del modelo
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu', kernel_regularizer=l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(trainY[0]), activation='softmax')
    ])

    # Compilación del modelo con función de pérdida y métricas
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Entrenamiento del modelo
    model.fit(trainX, trainY, epochs=250, batch_size=5, verbose=1)  # Ajusta según sea necesario

    # Evaluación del modelo en el conjunto de prueba
    scores = model.evaluate(testX, testY, verbose=0)
    print(f'Score for fold {fold_no+1}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')
    acc_per_fold.append(scores[1] * 100)
    loss_per_fold.append(scores[0])

# Muestra el rendimiento promedio
print('------------------------------------------------------------------------')
print('Puntuación por fold')
for i in range(0, len(acc_per_fold)):
    print(f'> Fold {i+1} - Loss: {loss_per_fold[i]} - Accuracy: {acc_per_fold[i]}%')
print('------------------------------------------------------------------------')
print('Promedio de todas las iteraciones:')
print(f'> Accuracy: {np.mean(acc_per_fold)} (+- {np.std(acc_per_fold)})')
print(f'> Loss: {np.mean(loss_per_fold)}')

#guarda el modelo en la ruta epecificada
model.save(model_path)
print('Done')