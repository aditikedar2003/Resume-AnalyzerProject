# auth.py

import streamlit as st
import psycopg2
from utils.security import hash_password, check_password
import os

# Setup DB connection
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

# Check if user exists
def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

# Insert new user
def insert_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        conn.commit()
    except Exception as e:
        st.error("Error: Email already exists or database error.")
    finally:
        cur.close()
        conn.close()

# Sign Up UI
def signup_ui():
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if name and email and password:
            hashed_pw = hash_password(password)
            insert_user(name, email, hashed_pw)
            st.success("Registration successful! Please log in.")
            st.session_state.page = "Login"
        else:
            st.error("Please fill all fields.")

# Login UI
def login_ui():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and check_password(password, user[3]):
            st.session_state.user_id = user[0]
            st.success("Login successful!")
            st.session_state.page = "Home"
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
