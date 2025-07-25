# views/linkedin.py

import streamlit as st
from utils.db import get_db_connection
from utils.session import get_current_user_id
from datetime import datetime

def show_linkedin_optimizer():
    st.header("LinkedIn Optimizer")

    user_id = get_current_user_id()
    if not user_id:
        st.warning("Please log in to access this feature.")
        return

    linkedin_summary = st.text_area("Paste your LinkedIn summary here")
    job_description = st.text_area("Paste the job description here")

    if st.button("Optimize"):
        if linkedin_summary and job_description:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO linkedin_profiles (summary, job_description, user_id, created_at)
                VALUES (%s, %s, %s, %s)
            """, (linkedin_summary, job_description, user_id, datetime.now()))
            conn.commit()
            conn.close()
            st.success("LinkedIn profile data saved and ready for optimization!")
            st.info("ℹ️ Optimization logic coming soon — currently saved to database.")
        else:
            st.warning("Both summary and job description are required!")
