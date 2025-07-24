import streamlit as st

# Import views
from views.auth import show_login_page, show_signup_page
from views.resume_scanner import show_resume_scanner
from views.cover_letter import show_cover_letter_analyzer
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from views.resume_builder import show_resume_builder
from views.dashboard import show_dashboard
from views.navbar import show_navbar

# Import session manager
from utils.session import get_user_id


# Initialize session states
if "user_id" not in st.session_state:
    st.session_state["user_id"] = get_user_id()

if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "login"

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

# Auth flow
if not st.session_state["user_id"]:
    if st.session_state["auth_mode"] == "login":
        show_login_page()
    else:
        show_signup_page()
else:
    # Show Navbar and appropriate page content
    show_navbar()

    if st.session_state["page"] == "dashboard":
        show_dashboard()
    elif st.session_state["page"] == "Resume Scanner":
        show_resume_scanner()
    elif st.session_state["page"] == "Cover Letter Analyzer":
        show_cover_letter_analyzer()
    elif st.session_state["page"] == "LinkedIn Optimizer":
        show_linkedin_optimizer()
    elif st.session_state["page"] == "Job Tracker":
        show_job_tracker()
    elif st.session_state["page"] == "Resume Builder":
        show_resume_builder()
    else:
        st.error("Page not found.")
