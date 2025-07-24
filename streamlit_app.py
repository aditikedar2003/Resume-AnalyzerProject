import streamlit as st
from views.auth import show_login_page, show_signup_page
from views.resume_scanner import show_resume_scanner
from views.cover_letter import show_cover_letter_analyzer
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from views.resume_builder import show_resume_builder
from views.dashboard import show_dashboard
from views.navbar import show_navbar

from utils.session import get_user_id  # ✅ THIS LINE FIXES THE ERROR
from views.auth import show_login_page, show_signup_page
# ...

# Check if user is logged in
user_id = get_user_id()

# Auth Flow
if not user_id:
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    if st.session_state["auth_mode"] == "login":
        show_login_page()
    else:
        show_signup_page()
