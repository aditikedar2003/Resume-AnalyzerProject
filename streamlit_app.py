import streamlit as st
from PIL import Image
import psycopg2
import base64
import os

# --- CONFIG ---
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# --- LOGO HEADER ---
col1, col2 = st.columns([1, 6])
with col1:
    logo = Image.open("assets/logo.png")  # Make sure this exists
    st.image(logo, width=100)
with col2:
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; flex-wrap: wrap;">
            <div style="font-size: 26px; font-weight: bold; color: #003366;">Resume Analyzer</div>
            <div style="margin-top: 10px;">
                <a href="#" style="margin-right: 20px; color: #003366; text-decoration: none;">Dashboard</a>
                <a href="#" style="margin-right: 20px; color: #003366; text-decoration: none;">Resume Scanner</a>
                <a href="#" style="margin-right: 20px; color: #003366; text-decoration: none;">Cover Letter</a>
                <a href="#" style="margin-right: 20px; color: #003366; text-decoration: none;">LinkedIn Optimizer</a>
                <a href="#" style="margin-right: 20px; color: #003366; text-decoration: none;">Pricing</a>
                <a href="#" style="margin-right: 20px; color: #003366; text-decoration: none;">Login</a>
                <a href="#" style="background-color: #003366; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none;">Sign Up</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Sidebar Navigation ---
menu = ["Dashboard", "Resume Scanner", "Cover Letter", "LinkedIn Optimizer", "Pricing", "Login", "Sign Up"]
choice = st.sidebar.radio("Navigate", menu)

# --- PostgreSQL Connection ---
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="resume_analyzer",
        user="postgres",
        password="yourpassword"  # replace with your actual DB password
    )

# --- Pages ---
if choice == "Dashboard":
    st.title("🎯 Welcome to Resume Analyzer")
    st.write("Tailor your resume, cover letter, and LinkedIn to stand out and land more interviews!")
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063829.png", width=150)

elif choice == "Resume Scanner":
    st.header("📄 Upload Your Resume & Job Description")
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_desc = st.text_area("Paste Job Description Here")

    if uploaded_resume and job_desc:
        st.success("Uploaded Successfully!")
        try:
            conn = connect_db()
            cur = conn.cursor()
            file_data = uploaded_resume.read()

            # Save resume
            cur.execute("INSERT INTO resumes (file_name, file_data, user_id) VALUES (%s, %s, %s)",
                        (uploaded_resume.name, psycopg2.Binary(file_data), 1))

            # Save JD
            cur.execute("INSERT INTO job_descriptions (title, content, user_id) VALUES (%s, %s, %s)",
                        ("JD for " + uploaded_resume.name, job_desc, 1))

            conn.commit()
            cur.close()
            conn.close()

            st.success("✅ Resume & JD saved to database!")

            # Mock analysis
            score = 88
            keywords = ["Python", "Django", "SQL", "REST API"]
            missing = [k for k in keywords if k.lower() not in job_desc.lower()]
            st.metric("Match Score", f"{score}%")
            st.write("**Missing Keywords:**", ", ".join(missing))

        except Exception as e:
            st.error(f"❌ Database error: {e}")
    else:
        st.info("Please upload both resume and JD.")

elif choice == "Cover Letter":
    st.header("📝 Cover Letter Scanner")
    st.write("Coming soon...")

elif choice == "LinkedIn Optimizer":
    st.header("🔗 LinkedIn Optimizer")
    st.write("Coming soon...")

elif choice == "Pricing":
    st.header("💰 Pricing Plans")
    st.write("""
    - **Free Tier**: 3 scans/month
    - **Premium**: ₹199/month for unlimited scans
    - **Enterprise**: Custom pricing
    """)

elif choice == "Login":
    st.subheader("🔐 Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("✅ Login feature will be added soon.")

elif choice == "Sign Up":
    st.subheader("🆕 Create a New Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                        (name, email, password, "user"))
            conn.commit()
            cur.close()
            conn.close()
            st.success("✅ Account created successfully!")
        except Exception as e:
            st.error(f"❌ Database error: {e}")
