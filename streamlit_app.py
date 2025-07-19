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

# ---------- HEADER (Logo + Navigation) ----------
st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between; padding: 10px 30px; background-color: #f5f5f5; border-radius: 8px; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center;'>
            <img src='https://raw.githubusercontent.com/aditikedar2003/your-repo-name/main/public/logo.png' width='60' style='margin-right: 15px;' />
            <h2 style='margin: 0;'>Resume Analyzer</h2>
        </div>
        <div>
            <a href='#Home' style='margin-right: 20px;'>Home</a>
            <a href='#Resume-Scanner' style='margin-right: 20px;'>Resume Scanner</a>
            <a href='#Cover-Letter' style='margin-right: 20px;'>Cover Letter</a>
            <a href='#LinkedIn' style='margin-right: 20px;'>LinkedIn</a>
            <a href='#Job-Tracker' style='margin-right: 20px;'>Job Tracker</a>
            <a href='#Login' style='margin-right: 20px;'>Login</a>
            <a href='#Signup'>Sign Up</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "Resume Scanner", "Cover Letter Scanner", "LinkedIn Optimizer", "Job Tracker"])

# ---------- HOME ----------
if app_mode == "Home":
    st.markdown("<h2 style='text-align:center;'>Resume Analyzer</h2>", unsafe_allow_html=True)
    st.image("https://www.jobscan.co/images/resume/illustration-ats@2x.png", use_column_width=True)
    st.markdown("""
        ## Features:
        - ✅ ATS Resume Scanner
        - ✅ Cover Letter Analyzer
        - ✅ Resume Builder (Coming Soon)
        - ✅ LinkedIn Optimizer
        - ✅ Job Tracker

        🧠 Upload your resume, match it with job descriptions and optimize everything from one platform!
    """)

# ---------- RESUME SCANNER ----------
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

# ---------- COVER LETTER ----------
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

# ---------- LINKEDIN OPTIMIZER ----------
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

# ---------- JOB TRACKER ----------
elif app_mode == "Job Tracker":
    st.header("📌 Job Application Tracker")
    st.write("Track your job applications here:")

    with st.form("job_tracker_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Job Role")
        status = st.selectbox("Application Status", ["Applied", "Interviewing", "Offer", "Rejected"])
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add to Tracker")
        if submitted:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO job_tracker (company, role, status, notes) VALUES (%s, %s, %s, %s)", (company, role, status, notes))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Job application saved!")

st.markdown("---")
st.markdown("Built with ❤️ by Aditi Kedar · Powered by Streamlit")
