# --- Resume Analyzer Full Project with Signup/Login and Back Button ---
import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# --- Database Configuration ---
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# --- Session State for Authentication ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None

# --- DB Connection ---
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        st.error("❌ DB Connection Failed: " + str(e))
        return None

# --- Back Button ---
def back_button():
    if st.button("⬅️ Back"):
        st.query_params.clear()
        st.rerun()

# --- Header Navigation ---
if st.session_state.logged_in:
    menu = ["Home", "Resume Scanner", "Cover Letter", "LinkedIn", "Job Tracker", "Logout"]
else:
    menu = ["Home", "Login", "Sign Up"]

app_mode = st.sidebar.radio("Navigation", menu)

# --- Pages ---
if app_mode == "Home":
    st.title("Welcome to Resume Analyzer")
    st.markdown("""
    ✅ ATS Resume Scanner\n
    ✅ Cover Letter Analyzer\n
    ✅ LinkedIn Optimizer\n
    ✅ Job Tracker
    """)

elif app_mode == "Sign Up":
    st.header("📝 Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if full_name and email and password:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("SELECT email FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    st.warning("Email already registered.")
                else:
                    cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)", (full_name, email, password))
                    conn.commit()
                    st.success("✅ Registered successfully. Please log in.")
                cur.close()
                conn.close()
        else:
            st.warning("Please fill all fields.")
    back_button()

elif app_mode == "Login":
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cur.fetchone()
            if user:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("✅ Login successful.")
                st.rerun()
            else:
                st.error("Invalid credentials.")
            cur.close()
            conn.close()
    back_button()

elif app_mode == "Logout":
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.success("Logged out successfully.")
    st.rerun()

elif app_mode == "Resume Scanner" and st.session_state.logged_in:
    st.header("📄 Upload Resume & Job Description")
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")
    if st.button("Analyze Resume"):
        if resume and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, content, uploaded_by) VALUES (%s, %s, %s)",
                            (resume.name, jd_text, st.session_state.user_email))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Resume and JD saved to database.")
            st.info("Sample Match Rate: 72% (replace with real scoring later)")
        else:
            st.warning("Please upload resume and enter JD.")
    back_button()

elif app_mode == "Cover Letter" and st.session_state.logged_in:
    st.header("✉️ Upload Cover Letter")
    cover_letter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"])
    if st.button("Analyze Cover Letter"):
        if cover_letter:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO cover_letters (filename, uploaded_by) VALUES (%s, %s)",
                            (cover_letter.name, st.session_state.user_email))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Cover Letter saved to database.")
            st.info("Tips: Add more keywords, tailor opening paragraph.")
        else:
            st.warning("Please upload a PDF file.")
    back_button()

elif app_mode == "LinkedIn" and st.session_state.logged_in:
    st.header("🔗 Optimize LinkedIn Profile")
    linkedin_text = st.text_area("Paste LinkedIn Summary")
    jd_text = st.text_area("Paste Job Description")
    if st.button("Analyze LinkedIn"):
        if linkedin_text and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO linkedin_profiles (summary, job_description, uploaded_by) VALUES (%s, %s, %s)",
                            (linkedin_text, jd_text, st.session_state.user_email))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ LinkedIn profile data saved.")
            st.info("Suggestions: Use action verbs, quantify results, match job keywords.")
        else:
            st.warning("Please complete both fields.")
    back_button()

elif app_mode == "Job Tracker" and st.session_state.logged_in:
    st.header("📌 Job Tracker")
    company = st.text_input("Company Name")
    position = st.text_input("Position")
    status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected", "Saved"])
    notes = st.text_area("Notes")
    if st.button("Save Job Entry"):
        if company and position:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO job_tracker (company, position, status, notes, user_email) VALUES (%s, %s, %s, %s, %s)",
                            (company, position, status, notes, st.session_state.user_email))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Job application saved.")
        else:
            st.warning("Company and Position are required.")
    back_button()
