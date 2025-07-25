# streamlit_app.py

import streamlit as st
from views.auth import show_login_page, show_signup_page


# Load custom theme
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Navigation
st.markdown("<h1 style='text-align: center;'>⭐ Resume Matcher</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Create a resume that tells your story using AI</p>", unsafe_allow_html=True)

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔑 Login"):
        st.session_state.page = "Login"
with col2:
    if st.button("📝 Sign Up"):
        st.session_state.page = "Signup"

# Route logic
if st.session_state.page == "Login":
    login_ui()

elif st.session_state.page == "Signup":
    signup_ui()

elif st.session_state.page == "Home" and st.session_state.user_id:
    st.success("You are logged in! 🎉")
    st.markdown("👉 Now go to Resume Scanner or Dashboard (coming next)")

elif st.session_state.page == "Home":
    st.markdown("Welcome! Please login or sign up to get started.")
