import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def getConnection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
    except Exception as e:
        print("no se puede conectar a la base de datos:", e)
        return None
    return conn

def unconnection(conn):
    conn.close()