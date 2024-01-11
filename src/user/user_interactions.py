from datetime import datetime
from config.database import connect_to_db


def get_user_id(chat_id):
    conn = connect_to_db()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM usuarios WHERE tele_chat_id = %s", (chat_id,))
    user_id = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return user_id[0] if user_id else None

def get_interaction_for_today(user_id):
    conn = connect_to_db()
    cur = conn.cursor()
    
    today = datetime.now().date()
    cur.execute("SELECT * FROM interacciones_usuario WHERE id_usuario = %s AND DATE(fecha) = %s", (user_id, today))
    interaction = cur.fetchone()

    cur.close()
    conn.close()
    
    if interaction:
        return reset_interactions_if_new_day(user_id, interaction)
    else:
        return None

def create_interaction_entry(user_id):
    conn = connect_to_db()
    cur = conn.cursor()

    today = datetime.now()
    cur.execute("INSERT INTO interacciones_usuario (id_usuario, interacciones, fecha) VALUES (%s, 0, %s)", (user_id, today))
    conn.commit()

    cur.close()
    conn.close()
    
    return user_id, 0, today

def increment_interaction_count(user_id):
    conn = connect_to_db()
    cur = conn.cursor()
    
    cur.execute("UPDATE interacciones_usuario SET interacciones = interacciones + 1 WHERE id_usuario = %s AND DATE(fecha) = %s", (user_id, datetime.now().date()))
    conn.commit()

    cur.close()
    conn.close()

def can_user_interact(chat_id):
    user_id = get_user_id(chat_id)
    if user_id is None:
        return False

    interaction = get_interaction_for_today(user_id)
    if interaction is None:
        interaction = create_interaction_entry(user_id)

    _, interacciones, _ = interaction

    if interacciones < 12:
        increment_interaction_count(user_id)
        return True
    else:
        return False


def reset_interactions_if_new_day(user_id, interaction):
    conn = connect_to_db()
    cur = conn.cursor()

    today = datetime.now().date()
    _, _, interaction_date = interaction

    if interaction_date < today:
        cur.execute("UPDATE interacciones_usuario SET interacciones = 0, fecha = %s WHERE id_usuario = %s", (today, user_id))
        conn.commit()
        interaction = (user_id, 0, today)

    cur.close()
    conn.close()

    return interaction

