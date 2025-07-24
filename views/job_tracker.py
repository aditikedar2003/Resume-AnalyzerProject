import streamlit as st
from utils.session import get_user_id
from utils.db import get_db_connection
import datetime

def show_job_tracker():
    user_id = get_user_id()
    if not user_id:
        st.warning("Please log in to use the Job Tracker.")
        return

    st.header("📌 Job Tracker")

    st.subheader("Add a New Job")

    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    application_date = st.date_input("Application Date", datetime.date.today())
    status = st.selectbox("Application Status", ["Applied", "Interview Scheduled", "Rejected", "Offer Received"])

    if st.button("Save Job"):
        if job_title and company:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO job_tracker (user_id, job_title, company, application_date, status, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, job_title, company, application_date, status, datetime.datetime.now())
            )
            conn.commit()
            conn.close()
            st.success("Saved successfully.")
        else:
            st.error("Please enter both Job Title and Company.")

    st.subheader("Your Tracked Jobs")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT job_title, company, application_date, status FROM job_tracker WHERE user_id = %s ORDER BY application_date DESC",
        (user_id,)
    )
    jobs = cur.fetchall()
    conn.close()

    if jobs:
        for job in jobs:
            st.markdown(f"**{job[0]}** at **{job[1]}**")
            st.write(f"📅 Applied on: {job[2]} | 📍 Status: {job[3]}")
            st.markdown("---")
    else:
        st.info("No jobs tracked yet.")
