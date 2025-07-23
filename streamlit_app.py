# streamlit_app.py
import streamlit as st
import psycopg2
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# DB Connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)
cursor = conn.cursor()

# Title Section
st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>JobBoost - AI-Powered Resume Analyzer</h1>
    <p style='text-align: center; font-size:18px;'>Optimize your Resume & Cover Letter to land your dream job faster 🚀</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Step 1: Upload Resume
st.subheader("1. Upload Resume (.pdf or .docx)")
resume_file = st.file_uploader("Choose your resume file", type=["pdf", "docx"])

# Step 2: Add Job Description
st.subheader("2. Paste Job Description")
jd_text = st.text_area("Paste the job description here")

# Step 3: Upload Cover Letter (Optional)
st.subheader("3. Upload Cover Letter (.pdf or .docx)")
cover_letter_file = st.file_uploader("Choose your cover letter file (optional)", type=["pdf", "docx"], key="cover")

if st.button("Analyze Now"):
    if resume_file and jd_text:
        def extract_text(file):
            if file.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(file)
                return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            elif file.name.endswith(".docx"):
                return docx2txt.process(file)
            return ""

        resume_text = extract_text(resume_file)
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100

        # Keyword analysis
        resume_tokens = set(resume_text.lower().split())
        jd_tokens = set(jd_text.lower().split())
        matched_keywords = list(resume_tokens & jd_tokens)
        missing_keywords = list(jd_tokens - resume_tokens)

        # Insert into DB
        cursor.execute("""
            INSERT INTO resumes (file_name, job_description, match_score, matched_keywords, missing_keywords, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            resume_file.name, jd_text, round(score, 2), ', '.join(matched_keywords), ', '.join(missing_keywords), datetime.now()
        ))
        conn.commit()

        st.success("✅ Resume and JD saved to database.")

        st.metric("🎯 Match Rate", f"{score:.2f}%")

        st.markdown(f"✅ **Matched Keywords** ({len(matched_keywords)}):")
        st.write(", ".join(matched_keywords))

        st.markdown(f"❌ **Missing Keywords** ({len(missing_keywords)}):")
        st.write(", ".join(missing_keywords))

        if cover_letter_file:
            cl_text = extract_text(cover_letter_file)
            cl_vecs = vectorizer.fit_transform([cl_text, jd_text])
            cl_score = cosine_similarity(cl_vecs[0:1], cl_vecs[1:2])[0][0] * 100
            st.metric("✉️ Cover Letter Match", f"{cl_score:.2f}%")

        st.markdown("---")
        st.success("✨ Analysis Complete!")

    else:
        st.error("❗ Please upload a resume and enter job description.")

# Resume Match History Section
st.markdown("""
    <h3 style='color:#2C3E50;'>📁 Resume Match History</h3>
""", unsafe_allow_html=True)

cursor.execute("SELECT file_name, match_score, created_at FROM resumes ORDER BY created_at DESC LIMIT 10")
data = cursor.fetchall()
if data:
    for row in data:
        st.write(f"📄 **{row[0]}** — 🟢 Score: {row[1]}% — 📅 {row[2].strftime('%Y-%m-%d %H:%M')}")
else:
    st.info("No resume history found.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>Built with ❤️ by JobBoost | Inspired by Jobscan</p>", unsafe_allow_html=True)
