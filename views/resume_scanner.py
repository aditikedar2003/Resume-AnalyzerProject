import streamlit as st

def show_resume_scanner():
    st.title("📄 Resume Scanner")
    st.markdown("Upload your **resume** and **job description**, and we'll tell you how well they match!")

    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
    job_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"], key="jobdesc")

    if resume_file and job_file:
        st.success("Both files uploaded successfully.")
        st.button("🔍 Analyze Match", type="primary")
        # TODO: Add resume-job matching logic here

    st.info("Need help writing a better resume? Try our Resume Builder tool!")
