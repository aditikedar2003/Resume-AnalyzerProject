import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

def insert_user(name, email, hashed_password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def insert_resume(file_name, file_data, jd_text, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO resumes (file_name, file_data, job_description, user_id) VALUES (%s, %s, %s, %s)",
                (file_name, file_data, jd_text, user_id))
    conn.commit()
    cur.close()
    conn.close()
