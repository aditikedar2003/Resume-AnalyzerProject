import streamlit as st
import requests
import base64
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import hashlib

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Global session
if "user" not in st.session_state:
    st.session_state.user = None

# Database connection function
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
        st.error("❌ Database connection failed: " + str(e))
        return None

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- HEADER NAVIGATION ---
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("https://raw.githubusercontent.com/aditikedar2003/Resume-AnalyzerProject/main/logo.png", width=100)
with col2:
    st.markdown("""
    <style>
    .header-nav {
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
    }
    .header-nav a {
        color: black;
        text-decoration: none;
        font-weight: bold;
    }
    .header-nav a:hover {
        color: #FF4B4B;
    }
    </style>
    <div class='header-nav'>
        <a href='/?app_mode=Home'>Home</a>
        <a href='/?app_mode=Resume Scanner'>Resume Scanner</a>
        <a href='/?app_mode=Cover Letter Scanner'>Cover Letter</a>
        <a href='/?app_mode=LinkedIn Optimizer'>LinkedIn</a>
        <a href='/?app_mode=Job Tracker'>Job Tracker</a>
        <a href='/?app_mode=Login'>Login</a>
        <a href='/?app_mode=Signup'>Sign Up</a>
    </div>
    <br><br>
    """, unsafe_allow_html=True)

# Get selected page from query params
app_mode = st.query_params.get("app_mode", "Home")

# --- Pages ---
if app_mode == "Home":
    st.markdown("<h1 style='text-align: center;'>Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("""
        ## Features:
        - ✅ ATS Resume Scanner
        - ✅ Cover Letter Analyzer
        - ✅ Resume Builder (Coming Soon)
        - ✅ LinkedIn Optimizer
        - ✅ Job Tracker

        🧠 Upload your resume, match it with job descriptions and optimize everything from one platform!
    """)

elif app_mode == "Resume Scanner":
    if st.session_state.user:
        st.header("📄 Upload Your Resume & Job Description")
        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        jd_text = st.text_area("Paste Job Description")

        if st.button("Analyze Resume"):
            if resume and jd_text:
                conn = connect_db()
                if conn:
                    cur = conn.cursor()
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS resumes (
                            id SERIAL PRIMARY KEY,
                            user_email VARCHAR(100),
                            filename VARCHAR(255),
                            job_description TEXT,
                            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    cur.execute("INSERT INTO resumes (user_email, filename, job_description) VALUES (%s, %s, %s)",
                                (st.session_state.user, resume.name, jd_text))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Resume and JD saved to database for user: " + st.session_state.user)
            else:
                st.warning("Please upload resume and enter JD.")
    else:
        st.warning("🔒 Please login to access the Resume Scanner.")

elif app_mode == "Cover Letter Scanner":
    if st.session_state.user:
        st.header("✉️ Upload Cover Letter")
        cover_letter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"])

        if st.button("Analyze Cover Letter"):
            if cover_letter:
                conn = connect_db()
                if conn:
                    cur = conn.cursor()
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS cover_letters (
                            id SERIAL PRIMARY KEY,
                            user_email VARCHAR(100),
                            filename VARCHAR(255),
                            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    cur.execute("INSERT INTO cover_letters (user_email, filename) VALUES (%s, %s)",
                                (st.session_state.user, cover_letter.name))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Cover Letter saved to database for user: " + st.session_state.user)
            else:
                st.warning("Please upload a PDF file.")
    else:
        st.warning("🔒 Please login to use this feature.")

elif app_mode == "LinkedIn Optimizer":
    if st.session_state.user:
        st.header("🔗 Optimize Your LinkedIn Profile")
        linkedin_text = st.text_area("Paste your LinkedIn Profile Summary or About section")
        jd_text = st.text_area("Paste a sample Job Description")

        if st.button("Analyze LinkedIn Profile"):
            if linkedin_text and jd_text:
                conn = connect_db()
                if conn:
                    cur = conn.cursor()
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS linkedin_profiles (
                            id SERIAL PRIMARY KEY,
                            user_email VARCHAR(100),
                            summary TEXT,
                            job_description TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    cur.execute("INSERT INTO linkedin_profiles (user_email, summary, job_description) VALUES (%s, %s, %s)",
                                (st.session_state.user, linkedin_text, jd_text))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ LinkedIn data saved for: " + st.session_state.user)
            else:
                st.warning("Please fill both fields.")
    else:
        st.warning("🔒 Please login to use this feature.")

elif app_mode == "Job Tracker":
    if st.session_state.user:
        st.header("📌 Job Application Tracker")
        company = st.text_input("Company Name")
        position = st.text_input("Job Title / Position")
        status = st.selectbox("Application Status", ["Applied", "Interview", "Offer", "Rejected", "Saved"])
        notes = st.text_area("Notes")

        if st.button("Save Job Entry"):
            if company and position:
                conn = connect_db()
                if conn:
                    cur = conn.cursor()
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS job_tracker (
                            id SERIAL PRIMARY KEY,
                            user_email VARCHAR(100),
                            company VARCHAR(255),
                            position VARCHAR(255),
                            status VARCHAR(50),
                            notes TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    cur.execute("INSERT INTO job_tracker (user_email, company, position, status, notes) VALUES (%s, %s, %s, %s, %s)",
                                (st.session_state.user, company, position, status, notes))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Job Entry saved.")
            else:
                st.warning("Company and Position are required.")
    else:
        st.warning("🔒 Please login to use the job tracker.")

elif app_mode == "Login":
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT email, password FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if user and hash_password(password) == user[1]:
                st.success("✅ Logged in successfully!")
                st.session_state.user = user[0]
            else:
                st.error("❌ Invalid email or password.")
            cur.close()
            conn.close()

elif app_mode == "Signup":
    st.header("📝 Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if full_name and email and password:
            conn = connect_db()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            full_name VARCHAR(100),
                            email VARCHAR(100) UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
                                (full_name, email, hash_password(password)))
                    conn.commit()
                    st.success("✅ Registration successful. Please login.")
                except psycopg2.errors.UniqueViolation:
                    st.error("❌ Email already registered.")
                except Exception as e:
                    st.error("❌ Registration failed: " + str(e))
                finally:
                    cur.close()
                    conn.close()
        else:
            st.warning("All fields are required.")

st.markdown("---")
st.markdown("Built with ❤️ by Aditi Kedar · Powered by Streamlit")
