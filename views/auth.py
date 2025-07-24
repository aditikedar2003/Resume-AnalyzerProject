import streamlit as st
from utils.db import get_db_connection
from utils.session import set_user_id

def show_signup_page():
    st.title("Create a New Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm:
            st.error("Passwords do not match.")
            return

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s) RETURNING id",
                        (full_name, email, password))
            user_id = cur.fetchone()[0]
            conn.commit()
            set_user_id(user_id)
            st.success("Account created! Please log in.")
            st.session_state["auth_mode"] = "login"
        except Exception as e:
            conn.rollback()
            st.error("Error creating account: Email may already be registered.")
        finally:
            cur.close()
            conn.close()

def show_login_page():
    st.title("Welcome Back")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            set_user_id(user[0])
            st.success("Logged in successfully!")
            st.session_state.page = "Resume Scanner"
        else:
            st.error("Invalid credentials")

    if st.button("Don't have an account? Sign Up"):
        st.session_state["auth_mode"] = "signup"
