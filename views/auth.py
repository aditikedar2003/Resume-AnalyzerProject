import streamlit as st
import bcrypt
from utils.db import get_user_by_email, insert_user

def show_login_page():
    st.header("🔐 Login to Resume Analyzer")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)

        if user:
            try:
                hashed_pw = user[3]  # Ensure this index exists
                if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            except IndexError:
                st.error("User data is corrupted or schema mismatch.")
        else:
            st.error("Invalid email or password.")

    st.markdown("Don't have an account? [Sign Up](#)", unsafe_allow_html=True)
    if st.button("Go to Sign Up"):
        st.session_state.page = 'signup'

def show_signup_page():
    st.header("📝 Sign Up for Resume Analyzer")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif get_user_by_email(email):
            st.error("User with this email already exists.")
        else:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            insert_user(full_name, email, hashed_pw)
            st.success("Account created successfully! Please login.")
            st.session_state.page = 'login'
            st.rerun()

    st.markdown("Already have an account? [Login](#)", unsafe_allow_html=True)
    if st.button("Go to Login"):
        st.session_state.page = 'login'
