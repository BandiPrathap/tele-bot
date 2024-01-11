from config.config import DATABASE_URL
import psycopg2

def connect_to_db():
    return psycopg2.connect(DATABASE_URL)

"""
# Ejecutar una consulta simple
try:
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("Conexión exitosa a PostgreSQL:")
    print(db_version)
except psycopg2.Error as e:
    print("Error al conectar a PostgreSQL:", e)
finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
"""