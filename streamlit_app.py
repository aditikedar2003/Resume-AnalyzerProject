import streamlit as st
from views.auth import show_login_page, show_signup_page
from views.resume_scanner import show_resume_scanner
from views.cover_letter import show_cover_letter_analyzer
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from utils.session import is_authenticated, logout

st.set_page_config(page_title="JobBoost Resume Analyzer", layout="wide")

def main():
    st.markdown("<h1 style='text-align:center; color:#2c3e50;'>JobBoost Resume Analyzer</h1>", unsafe_allow_html=True)
    menu = ["Home", "Login", "Sign Up", "Resume Scanner", "Cover Letter Analyzer", "LinkedIn Optimizer", "Job Tracker"]
    choice = st.selectbox("Navigate:", menu, index=0)

    if choice == "Home":
        st.write("Welcome to JobBoost! Please Login or Sign Up to use features.")
    elif choice == "Login":
        show_login_page()
    elif choice == "Sign Up":
        show_signup_page()
    elif choice == "Resume Scanner":
        if is_authenticated():
            show_resume_scanner()
        else:
            st.warning("Please log in first.")
    elif choice == "Cover Letter Analyzer":
        if is_authenticated():
            show_cover_letter_analyzer()
        else:
            st.warning("Please log in first.")
    elif choice == "LinkedIn Optimizer":
        if is_authenticated():
            show_linkedin_optimizer()
        else:
            st.warning("Please log in first.")
    elif choice == "Job Tracker":
        if is_authenticated():
            show_job_tracker()
        else:
            st.warning("Please log in first.")

    if is_authenticated():
        if st.button("Logout"):
            logout()
            st.success("Logged out successfully.")
            st.experimental_rerun()

if __name__ == "__main__":
    main()
