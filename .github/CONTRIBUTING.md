# streamlit_app.py

import streamlit as st
from PIL import Image
import os

# ---- Load Personal Image ----
image = Image.open("aditi-profile-resized.jpg")

# ---- Sidebar with Personal Info ----
st.sidebar.image(image, use_column_width=True)
st.sidebar.title("Aditi Kedar")
st.sidebar.markdown("📍 Pune, India")
st.sidebar.markdown("✉ [kedar.aditi07@gmail.com](mailto:kedar.aditi07@gmail.com)")
st.sidebar.markdown("🔗 [LinkedIn](https://www.linkedin.com/feed/)")
st.sidebar.markdown("💻 [GitHub](https://github.com/aditikedar2003)")
st.sidebar.markdown("📷 [Instagram](https://www.instagram.com/aditikedar11/)")

# ---- Main Content ----
st.title("Resume Matcher")
st.write("Upload your resume and job description to see how well they match.")

# Upload resume
resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description Here")

if resume_file and job_desc:
    st.success("Files uploaded successfully!")
    # Here you would add the parsing, matching and scoring logic
    st.write("🔍 Matching your resume against the job description...")
    
    # Mock score & keywords (for demo only)
    score = 87  # dummy score
    keywords = ["Java", "React", "SQL", "UI/UX", "API"]

    st.metric("Match Score", f"{score}%")
    st.write("**Missing Keywords:**")
    st.write(", ".join([k for k in keywords if k not in job_desc]))
else:
    st.warning("Please upload both resume and job description.")
