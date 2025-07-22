import streamlit as st
import psycopg2
import os
import hashlib
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# --- Session State ---
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# --- DB Config ---
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


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
        st.error(f"❌ Database connection failed: {e}")
        return None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(full_name, email, password):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s) RETURNING id", (full_name, email, hash_password(password)))
            user_id = cur.fetchone()[0]
            conn.commit()
            st.session_state.is_logged_in = True
            st.session_state.user_id = user_id
            st.session_state.user_name = full_name
            st.success("✅ Registration successful. Welcome!")
            st.experimental_rerun()
        except psycopg2.errors.UniqueViolation:
            st.warning("Email already registered.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cur.close()
            conn.close()


def login(email, password):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, full_name, password FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and user[2] == hash_password(password):
            st.session_state.is_logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]
            st.success(f"✅ Logged in as {user[1]}")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid email or password.")
        cur.close()
        conn.close()


def logout():
    st.session_state.is_logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = ""
    st.success("Logged out successfully.")
    st.experimental_rerun()

# --- Header Navigation ---
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

# --- Routing Logic ---
app_mode = st.query_params.get("app_mode", "Home")

if st.session_state.is_logged_in:
    st.markdown(f"### 👋 Welcome, {st.session_state.user_name}  ")
    if st.button("Logout"):
        logout()
else:
    if app_mode in ["Resume Scanner", "Cover Letter Scanner", "LinkedIn Optimizer", "Job Tracker"]:
        st.warning("⚠️ Please login to access this feature.")
        st.stop()

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

elif app_mode == "Signup":
    st.header("📝 Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if full_name and email and password:
            signup(full_name, email, password)
        else:
            st.warning("Please fill all fields.")

elif app_mode == "Login":
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:
            login(email, password)
        else:
            st.warning("Enter email and password.")

elif app_mode == "Resume Scanner":
    st.header("📄 Upload Your Resume & Job Description")
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")
    if st.button("Analyze Resume"):
        if resume and jd_text:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, content, user_id) VALUES (%s, %s, %s)", (resume.name, jd_text, st.session_state.user_id))
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
                cur.execute("INSERT INTO cover_letters (filename, user_id) VALUES (%s, %s)", (cover_letter.name, st.session_state.user_id))
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
                cur.execute("INSERT INTO linkedin_profiles (summary, job_description, user_id) VALUES (%s, %s, %s)", (linkedin_text, jd_text, st.session_state.user_id))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ LinkedIn Profile saved to database.")
                st.info("Profile Optimization Tips:\n- Use action verbs\n- Add measurable impact\n- Align with job role")
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
                cur.execute("INSERT INTO job_tracker (company, position, status, notes, user_id) VALUES (%s, %s, %s, %s, %s)", (company, position, status, notes, st.session_state.user_id))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Job Application saved successfully.")
        else:
            st.warning("Company and Position are required.")

# --- Back Navigation ---
if app_mode != "Home":
    if st.button("⬅️ Back to Home"):
        st.query_params["app_mode"] = "Home"
        st.experimental_rerun()

st.markdown("---")
st.markdown("Built with ❤️ by Aditi Kedar · Powered by Streamlit")
