import streamlit as st
from utils.session import get_user_id
from utils.db import get_db_connection

def show_dashboard():
    user_id = get_user_id()
    if not user_id:
        st.warning("Please log in to view your dashboard.")
        return

    st.header("📊 User Dashboard")

    conn = get_db_connection()
    cur = conn.cursor()

    st.subheader("Recent Resume Uploads")
    cur.execute("""
        SELECT filename, uploaded_at 
        FROM resumes 
        WHERE user_id = %s 
        ORDER BY uploaded_at DESC 
        LIMIT 5
    """, (user_id,))
    resumes = cur.fetchall()
    if resumes:
        for r in resumes:
            st.write(f"📄 {r[0]} — Uploaded at: {r[1]}")
    else:
        st.write("No resumes uploaded yet.")

    st.subheader("Recent Job Descriptions")
    cur.execute("""
        SELECT filename, uploaded_at 
        FROM job_descriptions 
        WHERE user_id = %s 
        ORDER BY uploaded_at DESC 
        LIMIT 5
    """, (user_id,))
    jobs = cur.fetchall()
    if jobs:
        for j in jobs:
            st.write(f"📝 {j[0]} — Uploaded at: {j[1]}")
    else:
        st.write("No job descriptions uploaded yet.")

    st.subheader("Recent Match Results")
    cur.execute("""
        SELECT r.filename, j.filename, m.match_percentage
        FROM match_results m
        JOIN resumes r ON m.resume_id = r.id
        JOIN job_descriptions j ON m.job_id = j.id
        WHERE r.user_id = %s
        ORDER BY m.matched_at DESC
        LIMIT 5
    """, (user_id,))
    matches = cur.fetchall()
    if matches:
        for m in matches:
            st.write(f"📌 Resume: {m[0]} | Job: {m[1]} | Match: {m[2]}%")
    else:
        st.write("No match results yet.")

    conn.close()
