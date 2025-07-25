import streamlit as st
from views.auth import show_login_page, show_signup_page
from views.dashboard import show_dashboard
from views.resume_scanner import show_resume_scanner
from views.cover_letter import show_cover_letter_scanner
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from utils.session import get_user_id, logout_user

st.set_page_config(page_title="Resume Analyzer", layout="centered")

def main():
    st.markdown("<h1 style='text-align:center;'>Resume Analyzer</h1>", unsafe_allow_html=True)
    user_id = get_user_id()

    if user_id:
        menu = ["Resume Scanner", "Cover Letter Scanner", "LinkedIn Optimizer", "Job Tracker", "Dashboard", "Logout"]
        choice = st.selectbox("Navigation", menu)

        if choice == "Resume Scanner":
            show_resume_scanner()
        elif choice == "Cover Letter Scanner":
            show_cover_letter_scanner()
        elif choice == "LinkedIn Optimizer":
            show_linkedin_optimizer()
        elif choice == "Job Tracker":
            show_job_tracker()
        elif choice == "Dashboard":
            show_dashboard()
        elif choice == "Logout":
            logout_user()
            st.success("Logged out successfully.")
            st.experimental_rerun()
    else:
        auth_mode = st.radio("Choose Option", ["Login", "Sign Up"])
        if auth_mode == "Login":
            show_login_page()
        else:
            show_signup_page()

if __name__ == "__main__":
    main()
