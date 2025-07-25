import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user
from utils.session import set_current_user


def show_signup_page():
    st.subheader("Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not (full_name and email and password and confirm):
            st.error("Please fill in all fields")
        elif password != confirm:
            st.warning("Passwords don’t match")
        else:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_id = insert_user(full_name, email, hashed)
            if user_id:
                st.success("Registration successful!")
                set_user_id(user_id)
                st.experimental_rerun()
            else:
                st.error("Email already registered.")

def show_login_page():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode(), user[3].encode()):
            st.success(f"Logged in as {user[1]}")
            set_user_id(user[0])
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
