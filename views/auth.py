import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user
from utils.session import set_user_id

def show_signup_page():
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        if name and email and password:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                insert_user(name, email, hashed_pw)
                st.success("Account created successfully! Please login.")
            except Exception as e:
                st.error("Error: Email already exists or database error.")
        else:
            st.warning("All fields are required.")

def show_login_page():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode(), user[3].encode()):
            st.success(f"Welcome, {user[1]}!")
            set_user_id(user[0])
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
