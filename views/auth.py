import streamlit as st
from utils.db import get_db_connection
from utils.session import set_user_id
import psycopg2.extras

def show_login_page():
    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            st.success("Login successful")
            set_user_id(user["id"])
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")


def show_signup_page():
    st.header("Sign Up")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s) RETURNING id", (full_name, email, password))
            user_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            st.success("Account created successfully. Please log in.")
            set_user_id(user_id)
            st.experimental_rerun()
        except Exception as e:
            st.error("Error: Email might already exist.")
