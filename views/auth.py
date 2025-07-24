import streamlit as st
from utils.db import get_user_by_email, insert_user
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and user[2] == hash_password(password):  # user[2] = password
            st.success("Login successful!")
            st.session_state["user_id"] = user[0]  # user[0] = id
            st.session_state["page"] = "dashboard"  # redirect to dashboard
        else:
            st.error("Invalid credentials.")

    st.markdown("Don't have an account? [Sign Up](#)", unsafe_allow_html=True)
    if st.button("Sign Up"):
        st.session_state["auth_mode"] = "signup"

def show_signup_page():
    st.title("Register")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
            return
        hashed_pw = hash_password(password)
        try:
            user_id = insert_user(full_name, email, hashed_pw)
            st.success("Registered successfully! Please log in.")
            st.session_state["auth_mode"] = "login"
        except Exception as e:
            st.error("Error registering user.")
            st.exception(e)

    if st.button("Back to Login"):
        st.session_state["auth_mode"] = "login"
