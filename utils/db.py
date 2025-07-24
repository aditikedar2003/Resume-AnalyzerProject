import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

def get_db_connection():
    conn = connect()
    cur = conn.cursor()
    return conn, cur
