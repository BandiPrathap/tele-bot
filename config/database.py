import os
import logging
from dotenv import load_dotenv
#from config.config import DATABASE_URL
import psycopg2

logging.basicConfig(level= logging.INFO)
load_dotenv()

def connect_to_db():
    database_url = os.getenv('DATABASE_URL')
    try:
        logging.info("conexión exitosa")
        return psycopg2.connect(database_url)
    except psycopg2.Error as e:
        logging.info(f"Error al conectar a la base de datos: {e}")
        raise

connect_to_db()

"""
def connect_to_db():
    return psycopg2.connect(DATABASE_URL)
"""
