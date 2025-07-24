import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user

def show_login_page():
    st.title("Login to Resume Analyzer")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]
            st.success(f"Welcome back, {user[1]}!")
            st.rerun()
        else:
            st.error("Invalid email or password")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = 'signup'
        st.rerun()

def show_signup_page():
    st.title("Sign Up for Resume Analyzer")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if not (name and email and password):
            st.warning("Please fill all fields")
            return

        existing = get_user_by_email(email)
        if existing:
            st.warning("Email already registered")
            return

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        insert_user(name, email, hashed_pw)
        st.success("Account created! Please log in.")
        st.session_state.page = 'login'
        st.rerun()
