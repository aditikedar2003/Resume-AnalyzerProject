import streamlit as st
from utils.session import get_user_id
from utils.db import get_db_connection
import datetime

def show_resume_builder():
    user_id = get_user_id()
    if not user_id:
        st.warning("Please log in to use the Resume Builder.")
        return

    st.header("📄 Resume Builder (Beta)")
    st.write("Fill in your details below and generate a basic resume.")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    summary = st.text_area("Professional Summary")

    st.subheader("Experience")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    experience_desc = st.text_area("Job Description")

    st.subheader("Education")
    degree = st.text_input("Degree")
    university = st.text_input("University")
    graduation_year = st.text_input("Year of Graduation")

    st.subheader("Skills")
    skills = st.text_area("List your key skills (comma separated)")

    if st.button("Generate Resume"):
        if name and email:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO resumes_built (user_id, name, email, phone, summary, job_title, company, experience_desc, degree, university, graduation_year, skills, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, name, email, phone, summary, job_title, company,
                experience_desc, degree, university, graduation_year, skills,
                datetime.datetime.now()
            ))
            conn.commit()
            conn.close()
            st.success("Resume details saved successfully!")
        else:
            st.error("Name and Email are required.")

    st.info("Note: This feature is currently in beta. PDF export coming soon!")
