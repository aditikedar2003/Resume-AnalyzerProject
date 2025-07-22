import streamlit as st
import requests
import base64
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

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

elif app_mode == "Job Tracker":
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
                cur.execute("INSERT INTO job_tracker (company, position, status, notes) VALUES (%s, %s, %s, %s)", (company, position, status, notes))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Job Application saved successfully.")
        else:
            st.warning("Company and Position are required.")

elif app_mode == "Login":
    st.header("🔐 Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Login")

elif app_mode == "Signup":
    st.header("📝 Sign Up")
    st.text_input("Full Name")
    st.text_input("Email")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Register")

st.markdown("---")
st.markdown("Built with ❤️ by Aditi Kedar · Powered by Streamlit")

