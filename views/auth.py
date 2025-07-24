# views/auth.py

import streamlit as st
from utils.db import get_user_by_email, insert_user  # adjust your import

def show_login_page():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and user["password"] == password:
            st.session_state["user_id"] = user["id"]
            st.session_state["page"] = "dashboard"  # ✅ set page
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password.")

    if st.button("Don't have an account? Sign Up"):
        st.session_state["auth_mode"] = "signup"
        st.experimental_rerun()


def show_signup_page():
    st.title("📝 Sign Up")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            user_id = insert_user(name, email, password)
            if user_id:
                st.session_state["user_id"] = user_id
                st.session_state["page"] = "dashboard"  # ✅ set page
                st.success("Sign-up successful!")
                st.experimental_rerun()
            else:
                st.error("Email already registered.")

    if st.button("Already have an account? Login"):
        st.session_state["auth_mode"] = "login"
        st.experimental_rerun()
