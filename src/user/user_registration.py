from src.user.user_verification import generate_otp, send_otp_email
from src.msg.msg import	get_msg
from config.database import connect_to_db
import psycopg2
import re
import logging

logging.basicConfig(level= logging.INFO)
"""
def is_user_registered(chat_id):
    # Aquí se conecta a la base de datos y verifica si el usuario está registrado
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE tele_chat_id = %s", (chat_id,))
    user_exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return user_exists
"""
def is_user_registered(chat_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Llama al procedimiento almacenado
        cur.callproc('is_user_registered', [chat_id])       
        # Obtiene el resultado del procedimiento almacenado
        user_exists = cur.fetchone()[0]
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        user_exists = None
    finally:
        if conn is not None:
            conn.close()
    return user_exists
"""
def register_user(correo, chat_id):
    # Aquí se conecta a la base de datos y registra el nuevo usuario
    conn = connect_to_db()
    cur = conn.cursor()
    # Primero, eliminar cualquier registro existente con el mismo correo electrónico
    cur.execute("DELETE FROM usuarios WHERE correo_electronico = %s;", (correo,))
    # Registra el usuario
    cur.execute("INSERT INTO usuarios (correo_electronico, tele_chat_id, fecha_registro) VALUES (%s, %s, NOW());", (correo, chat_id))
    conn.commit()
    cur.close()
    conn.close()
"""
def register_user(correo, chat_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Llama al procedimiento almacenado
        #cur.callproc('register_user', [correo, chat_id])
        cur.execute("CALL register_user(%s, %s)", (correo, chat_id))
        # Confirma los cambios
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()

"""
def unregister_user(chat_id):
    # Código para eliminar el usuario de la base de datos
    conn = connect_to_db()
    cur = conn.cursor()
    # Primero, eliminar las interacciones del usuario
    cur.execute("DELETE FROM interacciones_usuario WHERE id_usuario = (SELECT id FROM usuarios WHERE tele_chat_id = %s);", (chat_id,))
    cur.execute("DELETE FROM usuarios WHERE tele_chat_id = %s;", (chat_id,))
    conn.commit()
    cur.close()
    conn.close()
"""

def unregister_user(chat_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Llama al procedimiento almacenado
        #cur.callproc('unregister_user', [chat_id])
        cur.execute("CALL unregister_user(%s)", (chat_id,))
        # Confirma los cambios
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()


""" Solicita el correo al usuario """    
def get_mail_from_user(message, bot, estado):
    chat_id = message.chat.id
    correo = message.text
    #if re.match(r"^[a-zA-Z0-9._%+-]+@ug\.edu\.ec$", correo):
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo):
        logging.info('correo correcto')
        otp, secret = generate_otp()
        send_otp_email(correo, otp)
        bot.send_message(chat_id, get_msg('msg_otp_to_email'))
        return secret  # Devuelve y almacena el secreto en base32
    else:
        bot.send_message(chat_id, get_msg('msg_wrong_email'))
        return None


