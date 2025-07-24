import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user
from utils.session import set_user_id

def show_login_page():
    st.subheader("🔐 Login to Resume Analyzer")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            st.success("Login successful!")
            set_user_id(user[0])
            st.experimental_rerun()
        else:
            st.error("Invalid login details")

def show_signup_page():
    st.subheader("🧾 Sign Up for Resume Analyzer")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if not full_name or not email or not password:
            st.warning("Please fill all fields")
        elif get_user_by_email(email):
            st.error("Email already registered.")
        else:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_id = insert_user(full_name, email, hashed_pw.decode('utf-8'))
            if user_id:
                st.success("Registration successful! Please log in.")
                st.experimental_rerun()
            else:
                st.error("Registration failed.")
