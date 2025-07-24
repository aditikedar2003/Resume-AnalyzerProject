import psycopg2
import os

# Environment variables for DB connection
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# 🔌 Establish a connection to the PostgreSQL database
def connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ✅ For importing inside other files when you need both conn & cursor
def get_db_connection():
    """Return a new database connection and cursor."""
    conn = connect()
    cur = conn.cursor()
    return conn, cur

# 🔐 Check user credentials for login
def get_user_by_email(email):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

# 📝 Insert a new user into the database during registration
def insert_user(full_name, email, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s) RETURNING id",
        (full_name, email, password)
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id
