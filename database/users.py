import psycopg2
from utils.db import get_connection

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def create_user(email, hashed_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
