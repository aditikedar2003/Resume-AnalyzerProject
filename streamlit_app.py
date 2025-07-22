import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# --- DB Configuration ---
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

# --- Password Hash ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Header Navigation ---
def header_nav():
    st.markdown("""
    <style>
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
        font-weight: bold;
    }
    .nav-bar a {
        text-decoration: none;
        color: black;
    }
    .nav-bar a:hover {
        color: #FF4B4B;
    }
    </style>
    <div class="nav-bar">
        <a href="#" onclick="window.location.reload()">Home</a>
        <a href="#" onclick="window.location.reload()">Resume Scanner</a>
        <a href="#" onclick="window.location.reload()">Cover Letter</a>
        <a href="#" onclick="window.location.reload()">LinkedIn</a>
        <a href="#" onclick="window.location.reload()">Job Tracker</a>
        <a href="#" onclick="window.location.reload()">Login</a>
        <a href="#" onclick="window.location.reload()">Sign Up</a>
    </div><br><br>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("https://raw.githubusercontent.com/aditikedar2003/Resume-AnalyzerProject/main/logo.png", width=100)

    menu = ["Home", "Resume Scanner", "Cover Letter", "LinkedIn", "Job Tracker", "Login", "Signup"]
    selected = st.selectbox("📂 Navigation", menu, index=menu.index(st.session_state.page), label_visibility="collapsed")
    st.session_state.page = selected

# --- Pages ---
def page_home():
    st.title("🏠 Resume Analyzer")
    st.write("Welcome to your one-stop job preparation platform.")

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
                except:
                    st.error("Email already exists.")
                cur.close()
                conn.close()
        else:
            st.warning("Please fill all fields.")

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
            st.warning("Please fill all fields.")

def page_resume_scanner():
    st.markdown("◀️ [Back to Home](#)", unsafe_allow_html=True)
    st.header("📄 Resume Scanner")
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
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
                st.success("✅ Resume and JD saved.")
                st.info("Match Rate: 75% (Sample)")
        else:
            st.warning("Please upload a resume and job description.")

def page_cover_letter():
    st.markdown("◀️ [Back to Home](#)", unsafe_allow_html=True)
    st.header("✉️ Cover Letter Scanner")
    cover_letter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"])

    if st.button("Analyze"):
        if cover_letter:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO cover_letters (filename) VALUES (%s)", (cover_letter.name,))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Cover Letter saved.")
                st.info("Tip: Add more achievements and keywords.")
        else:
            st.warning("Please upload a PDF file.")

def page_linkedin():
    st.markdown("◀️ [Back to Home](#)", unsafe_allow_html=True)
    st.header("🔗 LinkedIn Optimizer")
    summary = st.text_area("Paste your LinkedIn Summary")
    jd = st.text_area("Paste Job Description")

    if st.button("Analyze"):
        if summary and jd:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO linkedin_profiles (summary, job_description) VALUES (%s, %s)", (summary, jd))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ LinkedIn data saved.")
                st.info("Add metrics, results, and strong verbs.")
        else:
            st.warning("Please fill both fields.")

def page_job_tracker():
    st.markdown("◀️ [Back to Home](#)", unsafe_allow_html=True)
    st.header("📌 Job Tracker")
    company = st.text_input("Company Name")
    position = st.text_input("Position")
    status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected", "Saved"])
    notes = st.text_area("Notes")

    if st.button("Save Job"):
        if company and position:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO job_tracker (company, position, status, notes) VALUES (%s, %s, %s, %s)",
                            (company, position, status, notes))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Job entry saved.")
        else:
            st.warning("Company and Position are required.")

# --- Render Header & Pages ---
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
        st.warning("Please log in first.")
        page_login()
elif st.session_state.page == "Cover Letter":
    page_cover_letter()
elif st.session_state.page == "LinkedIn":
    page_linkedin()
elif st.session_state.page == "Job Tracker":
    page_job_tracker()
