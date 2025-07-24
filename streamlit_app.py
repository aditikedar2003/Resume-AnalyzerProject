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

# Import session utils
from utils.session import get_user_id

# Set Streamlit page config
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# Get user session
user_id = get_user_id()

# 🔐 Auth Flow
if not user_id:
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    if st.session_state["auth_mode"] == "login":
        show_login_page()
    else:
        show_signup_page()

else:
    # ✅ Authenticated - show navbar and route
    show_navbar()

    page = st.session_state.get("selected_page", "Dashboard")

    if page == "Dashboard":
        show_dashboard()
    elif page == "Resume Scanner":
        show_resume_scanner()
    elif page == "Cover Letter Analyzer":
        show_cover_letter_analyzer()
    elif page == "LinkedIn Optimizer":
        show_linkedin_optimizer()
    elif page == "Job Tracker":
        show_job_tracker()
    elif page == "Resume Builder":
        show_resume_builder()
