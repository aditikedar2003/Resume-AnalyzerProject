import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

# Streamlit config
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# --- Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# --- Database Configuration ---
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def connect_db():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
    except Exception as e:
        st.error("Database connection failed.")
        return None

# --- Password Hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Navigation Header ---
def header_nav():
    st.markdown("""
    <style>
    .nav-links {display:flex; justify-content:center; gap:25px;}
    .nav-links a {text-decoration:none; font-weight:bold; color:#333;}
    .nav-links a:hover {color:#FF4B4B;}
    </style>
    <div class='nav-links'>
        <a href='#' onclick="window.location.reload();">Home</a>
        <a href='#' onclick="window.location.reload();">Resume Scanner</a>
        <a href='#' onclick="window.location.reload();">Cover Letter</a>
        <a href='#' onclick="window.location.reload();">LinkedIn</a>
        <a href='#' onclick="window.location.reload();">Job Tracker</a>
        <a href='#' onclick="window.location.reload();">Login</a>
        <a href='#' onclick="window.location.reload();">Sign Up</a>
    </div><br><br>
    """, unsafe_allow_html=True)

# --- Page: Home ---
def page_home():
    st.title("🏠 Resume Analyzer")
    st.write("Welcome to the smart job prep tool!")

# --- Page: Signup ---
def page_signup():
    st.header("📝 Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if full_name and email and password:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
                                (full_name, email, hash_password(password)))
                    conn.commit()
                    st.success("✅ Registered successfully! Redirecting to login...")
                    st.session_state.page = "Login"
                except Exception as e:
                    st.error("Email already exists.")
                cur.close()
                conn.close()
        else:
            st.warning("Please fill all fields.")

# --- Page: Login ---
def page_login():
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                            (email, hash_password(password)))
                user = cur.fetchone()
                cur.close()
                conn.close()
                if user:
                    st.success("✅ Logged in successfully!")
                    st.session_state.user_email = email
                    st.session_state.page = "Resume Scanner"
                else:
                    st.error("Invalid email or password.")
        else:
            st.warning("Please fill in both fields.")

# --- Page: Resume Scanner ---
def page_resume_scanner():
    st.markdown("◀️ [Back to Home](#)", unsafe_allow_html=True)
    st.header("📄 Resume Scanner")
    resume = st.file_uploader("Upload Resume", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    if st.button("Analyze"):
        if resume and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, content) VALUES (%s, %s)", (resume.name, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Resume and JD saved to database.")
                st.info("Match Rate: 78% (Simulated)")
        else:
            st.warning("Upload resume and enter job description.")

# --- Routing ---
header_nav()

if st.session_state.page == "Home":
    page_home()
elif st.session_state.page == "Signup":
    page_signup()
elif st.session_state.page == "Login":
    page_login()
elif st.session_state.page == "Resume Scanner":
    if st.session_state.user_email:
        page_resume_scanner()
    else:
        st.warning("Please log in to access Resume Scanner.")
        page_login()

# --- Navigation Control ---
with st.sidebar:
    st.write("📂 Navigation")
    if st.button("🏠 Home"):
        st.session_state.page = "Home"
    if st.button("📝 Sign Up"):
        st.session_state.page = "Signup"
    if st.button("🔐 Login"):
        st.session_state.page = "Login"
    if st.session_state.user_email:
        if st.button("📄 Resume Scanner"):
            st.session_state.page = "Resume Scanner"
        if st.button("🚪 Logout"):
            st.session_state.user_email = None
            st.session_state.page = "Home"
