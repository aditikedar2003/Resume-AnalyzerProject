import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import hashlib
from utils.session import get_user_id, set_user_id, clear_user_id
from views.auth import show_login_page, show_signup_page
from views.resume_matcher import show_resume_matcher
from views.cover_letter import show_cover_letter_analyzer
from views.linkedin import show_linkedin_optimizer
from views.job_tracker import show_job_tracker
from views.resume_builder import show_resume_builder
from views.dashboard import show_dashboard
from views.navbar import show_navbar

# Load environment variables
load_dotenv()

# DB connection settings
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

# App Config
st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session State
if 'page' not in st.session_state:
    st.session_state.page = 'Login'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Navbar (Top header navigation)
if st.session_state.user_id:
    show_navbar()

# Routing
page = st.session_state.page

if page == 'Login':
    show_login_page()
elif page == 'Sign Up':
    show_signup_page()
elif page == 'Resume Scanner':
    show_resume_matcher()
elif page == 'Cover Letter Analyzer':
    show_cover_letter_analyzer()
elif page == 'LinkedIn Optimizer':
    show_linkedin_optimizer()
elif page == 'Job Tracker':
    show_job_tracker()
elif page == 'Resume Builder':
    show_resume_builder()
elif page == 'Dashboard':
    show_dashboard()

# Footer
st.markdown("""
    <style>
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
