# Streamlit Resume Analyzer App (Uniquely Designed like Jobscan, not copied)

import streamlit as st
import base64
from utils.resume_matcher import calculate_match_score
from utils.db import insert_resume_result, get_user_submissions
from utils.ui import show_header, show_navigation, show_back_button
from utils.auth import is_logged_in, redirect_to_login
import os

# Set page config
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Session check
if not is_logged_in():
    redirect_to_login()

# UI - Header & Navigation
show_header()
show_navigation()

# Main Section - Resume Scanner
st.markdown("""
    <div style='padding: 1rem 0; text-align: center;'>
        <h2 style='font-size: 2rem;'>📄 Resume Scanner</h2>
        <p style='color: #666;'>Optimize your resume for Applicant Tracking Systems (ATS) just like Jobscan</p>
    </div>
""", unsafe_allow_html=True)

with st.form("resume_form"):
    uploaded_resume = st.file_uploader("Upload Your Resume (.pdf, .docx)", type=["pdf", "docx"])
    job_description = st.text_area("Paste the Job Description Here", height=250)
    submit_btn = st.form_submit_button("🔍 Scan Now")

if submit_btn:
    if uploaded_resume and job_description:
        with st.spinner("Analyzing resume with AI ✨"):
            resume_text = uploaded_resume.read().decode("utf-8", errors="ignore")
            match_score, matched_keywords, missing_keywords = calculate_match_score(resume_text, job_description)

            # Save result to DB
            insert_resume_result(st.session_state.user_id, resume_text, job_description, match_score)

            # Show Results
            st.success(f"✅ Match Score: {match_score}%")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✔️ Keywords Found")
                st.write(", ".join(matched_keywords))

            with col2:
                st.subheader("❌ Keywords Missing")
                st.write(", ".join(missing_keywords))
    else:
        st.warning("Please upload a resume and paste a job description.")

# Back Button
show_back_button("Dashboard")
