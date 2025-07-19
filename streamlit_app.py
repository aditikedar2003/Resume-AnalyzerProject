import streamlit as st
import requests
import base64
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Database configuration from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "resume_analyzer")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Test@123")

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
        st.error("Database connection failed: " + str(e))
        return None

# Sidebar Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "Resume Scanner", "Cover Letter Scanner", "LinkedIn Optimizer", "Job Tracker"])

# App Header with logo
st.markdown("""
    <div style='display: flex; align-items: center;'>
        <img src='https://raw.githubusercontent.com/aditikedar2003/Resume-Analyzer-Final/main/logo.png' width='60' style='margin-right: 10px;'>
        <h1 style='display:inline;'>Resume Analyzer</h1>
    </div>
""", unsafe_allow_html=True)

# Home Page
if app_mode == "Home":
    st.markdown("""
        <center><img src='https://www.jobscan.co/images/resume/illustration-ats@2x.png' width='70%'/></center>
    """, unsafe_allow_html=True)

    st.markdown("""
        ## Features:
        - ✅ ATS Resume Scanner
        - ✅ Cover Letter Analyzer
        - ✅ Resume Builder (Coming Soon)
        - ✅ LinkedIn Optimizer
        - ✅ Job Tracker

        🧠 Upload your resume, match it with job descriptions and optimize everything from one platform!
    """)

# Resume Scanner
elif app_mode == "Resume Scanner":
    st.header("📄 Upload Your Resume & Job Description")

    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):
        if resume and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, job_description) VALUES (%s, %s)", (resume.name, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Resume and JD saved to database.")
            st.info("Match Rate: 72% (Sample)")
        else:
            st.warning("Please upload resume and enter JD.")

# Cover Letter Scanner
elif app_mode == "Cover Letter Scanner":
    st.header("✉️ Upload Cover Letter")

    cover_letter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"])
    if st.button("Analyze Cover Letter"):
        if cover_letter:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO cover_letters (filename) VALUES (%s)", (cover_letter.name,))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Cover Letter saved to database.")
            st.info("Tips: Add more keywords, tailor opening paragraph.")
        else:
            st.warning("Please upload a PDF file.")

# LinkedIn Optimizer
elif app_mode == "LinkedIn Optimizer":
    st.header("🔗 Optimize Your LinkedIn Profile")

    linkedin_text = st.text_area("Paste your LinkedIn Profile Summary or About section")
    jd_text = st.text_area("Paste a sample Job Description")

    if st.button("Analyze LinkedIn Profile"):
        if linkedin_text and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO linkedin_profiles (summary, job_description) VALUES (%s, %s)", (linkedin_text, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ LinkedIn Profile saved to database.")
            st.info("Profile Optimization Suggestions:\n- Add more action verbs\n- Include measurable results\n- Tailor to role keywords")
        else:
            st.warning("Please enter both LinkedIn content and job description.")

# Job Tracker (UI placeholder)
elif app_mode == "Job Tracker":
    st.header("📌 Job Application Tracker")
    st.info("Coming Soon: Add jobs, track status, and notes here!")

st.markdown("---")
st.markdown("Built with ❤️ by Aditi Kedar · Powered by Streamlit")
