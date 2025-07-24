# streamlit_app.py

import streamlit as st
from views.auth import show_login_page, show_signup_page
from views.resume_scanner import show_resume_scanner
from views.cover_letter import show_cover_letter_analyzer
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from views.resume_builder import show_resume_builder
from views.dashboard import show_dashboard
from views.navbar import show_navbar

# ✅ Handle user session
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "login"

user_id = st.session_state["user_id"]

if not user_id:
    if st.session_state["auth_mode"] == "login":
        show_login_page()
    else:
        show_signup_page()
else:
    # ✅ Logged in: show main app
    show_navbar()
    page = st.session_state.get("page", "dashboard")

    if page == "dashboard":
        show_dashboard()
    elif page == "resume_scanner":
        show_resume_scanner()
    elif page == "cover_letter":
        show_cover_letter_analyzer()
    elif page == "linkedin":
        show_linkedin_optimizer()
    elif page == "job_tracker":
        show_job_tracker()
    elif page == "resume_builder":
        show_resume_builder()
