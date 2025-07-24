import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        cursor_factory=psycopg2.extras.RealDictCursor
    )


def insert_user(full_name, email, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (full_name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (full_name, email, password_hash))
    user_id = cur.fetchone()['id']
    conn.commit()
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    conn.close()
    return user
