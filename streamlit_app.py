# ✅ Here's the complete updated codebase you need to fix your login + registration + database connection errors:

# ===========================
# ✅ streamlit_app.py
# ===========================
import streamlit as st
from views.auth import show_login_page, show_signup_page

st.set_page_config(page_title="JobBoost | Resume Analyzer", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if st.session_state.page == 'login':
    show_login_page()
elif st.session_state.page == 'signup':
    show_signup_page()


# ===========================
# ✅ views/auth.py
# ===========================
import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user

def show_login_page():
    st.title("Login to Resume Analyzer")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user:
            stored_password = user[3]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                st.success("Login successful!")
                st.session_state['user'] = {"id": user[0], "name": user[1], "email": user[2]}
                st.switch_page("pages/resume_scanner.py")
            else:
                st.error("Invalid password.")
        else:
            st.error("User not found.")

    st.markdown("Don't have an account? [Sign up](#)")
    if st.button("Sign Up"):
        st.session_state.page = 'signup'

def show_signup_page():
    st.title("Register for Resume Analyzer")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            user_id = insert_user(full_name, email, hashed_pw)
            st.success("Registration successful! Please login.")
            st.session_state.page = 'login'
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")

    st.markdown("Already have an account? [Login](#)")
    if st.button("Back to Login"):
        st.session_state.page = 'login'


# ===========================
# ✅ utils/db.py
# ===========================
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    return conn

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, email, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def insert_user(full_name, email, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (full_name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (full_name, email, password_hash))
    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id
