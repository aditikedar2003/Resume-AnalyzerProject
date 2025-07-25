# streamlit_app.py
import streamlit as st
from views.auth import show_login_page, show_signup_page
from views.resume_scanner import show_resume_scanner
from views.cover_letter import show_cover_letter_analyzer
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from views.dashboard import show_dashboard
from utils.session import is_logged_in, logout, get_current_user

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Header Navigation
menu = ["Resume Scanner", "Cover Letter Analyzer", "LinkedIn Optimizer", "Job Tracker", "Dashboard", "Logout"]

if "page" not in st.session_state:
    st.session_state.page = "Login"

if st.session_state.page == "Login":
    show_login_page()

elif st.session_state.page == "Signup":
    show_signup_page()

elif st.session_state.page in menu:
    with st.sidebar:
        st.title("Resume Analyzer")
        selected = st.selectbox("Navigate", menu)
        st.markdown(f"**Logged in as:** {get_current_user()['name']}")

    if selected == "Resume Scanner":
        show_resume_scanner()
    elif selected == "Cover Letter Analyzer":
        show_cover_letter_analyzer()
    elif selected == "LinkedIn Optimizer":
        show_linkedin_optimizer()
    elif selected == "Job Tracker":
        show_job_tracker()
    elif selected == "Dashboard":
        show_dashboard()
    elif selected == "Logout":
        logout()
        st.session_state.page = "Login"
        st.experimental_rerun()

# Back to Login/Signup switching
if not is_logged_in():
    st.sidebar.title("Account")
    if st.sidebar.button("Sign Up"):
        st.session_state.page = "Signup"
        st.experimental_rerun()
    if st.sidebar.button("Login"):
        st.session_state.page = "Login"
        st.experimental_rerun()
