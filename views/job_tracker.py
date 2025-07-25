# views/job_tracker.py

import streamlit as st
from utils.db import get_db_connection
from utils.session import get_current_user_id
from datetime import datetime

def show_job_tracker():
    st.header("Job Tracker")

    user_id = get_current_user_id()
    if not user_id:
        st.warning("Please log in to access this feature.")
        return

    st.subheader("Add New Job Entry")
    company = st.text_input("Company Name")
    position = st.text_input("Job Position")
    status = st.selectbox("Application Status", ["Applied", "Interviewing", "Offered", "Rejected", "Saved"])
    notes = st.text_area("Notes")

    if st.button("Add Job"):
        if company and position:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO job_tracker (company, position, status, notes, user_id, tracked_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (company, position, status, notes, user_id, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Job entry added!")
        else:
            st.warning("Please fill in at least company and position.")

    # Display existing jobs
    st.subheader("Your Tracked Jobs")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT company, position, status, notes, tracked_at FROM job_tracker WHERE user_id = %s ORDER BY tracked_at DESC", (user_id,))
    jobs = cur.fetchall()
    conn.close()

    if jobs:
        for job in jobs:
            st.write(f"**Company:** {job[0]}")
            st.write(f"**Position:** {job[1]}")
            st.write(f"**Status:** {job[2]}")
            st.write(f"**Notes:** {job[3]}")
            st.write(f"**Tracked At:** {job[4].strftime('%Y-%m-%d %H:%M')}")
            st.markdown("---")
    else:
        st.info("No jobs tracked yet.")
