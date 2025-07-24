import streamlit as st
import bcrypt
from db import get_user_by_email, insert_user


def show_login_page():
    st.title("Login to Resume Analyzer")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)

        if user:
            stored_password_hash = user['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                st.success("Login successful!")
                st.session_state.user = {
                    "id": user['id'],
                    "full_name": user['full_name'],
                    "email": user['email']
                }
                st.switch_page("pages/resume_scanner.py")
            else:
                st.error("Invalid password.")
        else:
            st.error("User not found.")

    st.markdown("Don't have an account? [Sign up](#)", unsafe_allow_html=True)


def show_signup_page():
    st.title("Create a New Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            user_id = insert_user(full_name, email, hashed_password)
            st.success("Account created! Please log in.")
            st.switch_page("streamlit_app.py")
        except Exception as e:
            st.error("Error: " + str(e))
