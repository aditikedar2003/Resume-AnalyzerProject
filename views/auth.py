import streamlit as st
from utils.db import get_db_connection
from utils.session import set_user_id
from utils.security import hash_password, verify_password

def show_login_page():
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user and verify_password(password, user[1]):
            set_user_id(user[0])
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")

def show_signup_page():
    st.subheader("Sign Up")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        hashed_pw = hash_password(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
                        (full_name, email, hashed_pw))
            conn.commit()
            st.success("Sign-up successful. Please log in.")
            st.switch_page("streamlit_app.py")  # Optional redirect
        except Exception as e:
            conn.rollback()
            st.error("Email already exists or database error.")
        finally:
            cur.close()
            conn.close()
