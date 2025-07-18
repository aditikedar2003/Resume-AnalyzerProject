
import streamlit as st
import requests
import base64
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env if exists
if os.path.exists(".env"):
    load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# --- Branding ---
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.image("https://raw.githubusercontent.com/aditikedar2003/Resume-Analyzer-Final/main/logo.png", width=100)

with col2:
    st.markdown("<h1 style='padding-top: 20px;'>Resume Analyzer – JobScan Style SaaS</h1>", unsafe_allow_html=True)

# --- Database configuration ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "resume_analyzer")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Test@123")

# --- Database connection ---
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
        st.error("❌ Database connection failed: " + str(e))
        return None

# --- Sidebar ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "Resume Scanner", "Cover Letter Scanner", "LinkedIn Optimizer", "Job Tracker"])

# --- Home ---
if app_mode == "Home":
    st.image("https://www.jobscan.co/images/resume/illustration-ats@2x.png", use_column_width=True)
    st.markdown("""
        ### 🚀 Features:
        - ✅ ATS Resume Scanner
        - ✅ Cover Letter Analyzer
        - 🛠️ Resume Builder *(Coming Soon)*
        - ✅ LinkedIn Optimizer
        - ✅ Job Tracker

        💡 Upload your resume, match it with job descriptions, and optimize everything from one platform!
    """)

# --- Resume Scanner ---
elif app_mode == "Resume Scanner":
    st.header("📄 Upload Resume & Job Description")
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    if st.button("🔍 Analyze Resume"):
        if resume and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, job_description) VALUES (%s, %s)", (resume.name, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Resume and JD saved to database.")
                st.info("💡 Match Rate: 72% (sample)")
        else:
            st.warning("⚠️ Please upload a resume and enter the job description.")

# --- Cover Letter Scanner ---
elif app_mode == "Cover Letter Scanner":
    st.header("✉️ Upload Cover Letter")
    cover_letter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"])

    if st.button("🔍 Analyze Cover Letter"):
        if cover_letter:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO cover_letters (filename) VALUES (%s)", (cover_letter.name,))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Cover Letter saved to database.")
                st.info("💡 Tips: Add more keywords, tailor the opening paragraph.")
        else:
            st.warning("⚠️ Please upload a PDF file.")

# --- LinkedIn Optimizer ---
elif app_mode == "LinkedIn Optimizer":
    st.header("🔗 Optimize LinkedIn Profile")
    linkedin_text = st.text_area("Paste your LinkedIn 'About' section")
    jd_text = st.text_area("Paste a Job Description")

    if st.button("🔍 Analyze LinkedIn Profile"):
        if linkedin_text and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO linkedin_profiles (summary, job_description) VALUES (%s, %s)", (linkedin_text, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ LinkedIn Profile saved to database.")
                st.info("""
                💡 Optimization Suggestions:
                - Add more action verbs
                - Include measurable results
                - Match keywords from the job role
                """)
        else:
            st.warning("⚠️ Please enter both LinkedIn text and job description.")

# --- Job Tracker (Coming Soon) ---
elif app_mode == "Job Tracker":
    st.header("📌 Job Application Tracker")
    st.info("🛠️ Coming Soon: Track your job applications, statuses, and notes here.")

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align: center;'>Built with ❤️ by <b>Aditi Kedar</b> · Powered by Streamlit</div>", unsafe_allow_html=True)
