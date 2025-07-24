import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user

def show_login_page():
    st.subheader("🔐 Login to Resume Analyzer")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            st.success("✅ Login successful!")
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.full_name = user[1]
        else:
            st.error("❌ Invalid email or password")

    st.markdown("Don't have an account? [Sign up here](#)", unsafe_allow_html=True)
    if st.button("Go to Sign Up"):
        st.session_state.page = "signup"


def show_signup_page():
    st.subheader("🆕 Create Your Resume Analyzer Account")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("❌ Passwords do not match")
            return

        existing_user = get_user_by_email(email)
        if existing_user:
            st.error("❌ Email already registered")
            return

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_id = insert_user(full_name, email, password_hash)
        st.success("✅ Account created successfully! Please log in.")
        st.session_state.page = "login"

    st.markdown("Already have an account? [Login here](#)", unsafe_allow_html=True)
    if st.button("Go to Login"):
        st.session_state.page = "login"
