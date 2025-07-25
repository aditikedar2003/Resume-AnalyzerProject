import streamlit as st
from utils.security import hash_password, verify_password
from database.users import get_user_by_email, create_user


def show_login_page():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)  # ✅ This line should be inside the button click block

        if user and verify_password(password, user["password"]):
            st.session_state.user_id = user["id"]
            st.success("Login successful!")
            st.session_state.page = "Home"
        else:
            st.error("Invalid credentials.")


def show_signup_page():
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        hashed = hash_password(password)
        success = create_user(name, email, hashed)

        if success:
            st.success("Account created! Please log in.")
            st.session_state.page = "Login"
        else:
            st.error("Email already exists or error occurred.")
