import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Environment Variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Session Initialization
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "user" not in st.session_state:
    st.session_state.user = None

# Database connection
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# --- Header Navigation ---
def header_nav():
    st.markdown("""
    <style>
        div[data-testid="column"] > div {
            display: flex;
            gap: 20px;
            justify-content: center;
        }
        button[kind="secondary"] {
            background-color: #f0f2f6;
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("https://raw.githubusercontent.com/aditikedar2003/Resume-AnalyzerProject/main/logo.png", width=90)
    with col2:
        nav_items = ["Home", "Resume Scanner", "Cover Letter", "LinkedIn", "Job Tracker"]
        if st.session_state.user:
            nav_items.append("Logout")
        else:
            nav_items.extend(["Login", "Signup"])

        for item in nav_items:
            if st.button(item):
                if item == "Logout":
                    st.session_state.user = None
                    st.success("✅ Logged out successfully.")
                    st.session_state.page = "Home"
                else:
                    st.session_state.page = item
                st.experimental_rerun()

# --- Page Rendering ---
def show_home():
    st.markdown("<h1 style='text-align: center;'>Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("""
    ## Features:
    - ✅ ATS Resume Scanner
    - ✅ Cover Letter Analyzer
    - ✅ LinkedIn Optimizer
    - ✅ Job Tracker

    📤 Upload your resume, match it with job descriptions, and optimize everything from one platform!
    """)

def show_signup():
    st.header("📝 Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if full_name and email and password:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)", (full_name, email, password))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Registration successful. Redirecting to login...")
                st.session_state.page = "Login"
                st.experimental_rerun()
            except psycopg2.errors.UniqueViolation:
                st.error("⚠️ Email already exists.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("All fields are required.")

def show_login():
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
                user = cur.fetchone()
                cur.close()
                conn.close()
                if user:
                    st.session_state.user = {"id": user[0], "full_name": user[1], "email": user[2]}
                    st.success("✅ Login successful. Redirecting to Resume Scanner...")
                    st.session_state.page = "Resume Scanner"
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid credentials.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Enter both email and password.")

def show_resume_scanner():
    st.header("📄 Resume Scanner")
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):
        if resume and jd_text:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, content) VALUES (%s, %s)", (resume.name, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Resume and JD saved to database.")
                st.info("Match Rate: 72% (Sample)")  # To be replaced with actual NLP score later
            except Exception as e:
                st.error("❌ Failed to save data: " + str(e))
        else:
            st.warning("Please upload resume and enter JD.")

def show_cover_letter():
    st.header("✉️ Cover Letter Analyzer")
    cover_letter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"])
    if st.button("Analyze Cover Letter"):
        if cover_letter:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO cover_letters (filename) VALUES (%s)", (cover_letter.name,))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Cover Letter saved to database.")
                st.info("Tips: Add more keywords, tailor your opening paragraph.")
            except Exception as e:
                st.error("❌ Failed to save: " + str(e))
        else:
            st.warning("Please upload a PDF.")

def show_linkedin():
    st.header("🔗 LinkedIn Optimizer")
    linkedin_text = st.text_area("Paste LinkedIn Summary/About")
    jd_text = st.text_area("Paste Job Description")
    if st.button("Analyze LinkedIn"):
        if linkedin_text and jd_text:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO linkedin_profiles (summary, job_description) VALUES (%s, %s)", (linkedin_text, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ LinkedIn data saved.")
                st.info("Optimization Tip: Add measurable results, action verbs, and match role keywords.")
            except Exception as e:
                st.error("❌ Error saving data: " + str(e))
        else:
            st.warning("Both fields are required.")

def show_job_tracker():
    st.header("📌 Job Tracker")
    company = st.text_input("Company Name")
    position = st.text_input("Job Title / Position")
    status = st.selectbox("Application Status", ["Applied", "Interview", "Offer", "Rejected", "Saved"])
    notes = st.text_area("Notes")

    if st.button("Save Job Entry"):
        if company and position:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO job_tracker (company, position, status, notes) VALUES (%s, %s, %s, %s)", (company, position, status, notes))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Job Application saved.")
            except Exception as e:
                st.error("❌ Error: " + str(e))
        else:
            st.warning("Company and Position are required.")

# --- Main Execution ---
header_nav()

# Render Pages
page = st.session_state.page
if page == "Home":
    show_home()
elif page == "Signup":
    show_signup()
elif page == "Login":
    show_login()
elif page == "Resume Scanner":
    show_resume_scanner()
elif page == "Cover Letter":
    show_cover_letter()
elif page == "LinkedIn":
    show_linkedin()
elif page == "Job Tracker":
    show_job_tracker()
