import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, email, password FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close(); conn.close()
    return user

def insert_user(full_name, email, password_hash):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s) RETURNING id",
            (full_name, email, password_hash)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close(); conn.close()
        return user_id
    except psycopg2.errors.UniqueViolation:
        return None
