import streamlit as st
from utils.db import get_db_connection
from PyPDF2 import PdfReader
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2
import datetime

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    resume_keywords = set(resume_text.lower().split())
    jd_keywords = set(jd_text.lower().split())
    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords

    return round(similarity * 100, 2), matched, missing

def save_resume_result(user_id, resume_text, jd_text, score):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resumes (user_id, resume_text, jd_text, match_score, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, resume_text, jd_text, score, datetime.datetime.now()))
    conn.commit()
    cur.close(); conn.close()

def show_resume_scanner():
    st.subheader("Upload Resume and Job Description")
    
    user_id = st.session_state.get("user_id")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])
    job_description = st.text_area("Paste Job Description here")

    if st.button("Analyze"):
        if not uploaded_file or not job_description:
            st.error("Please upload a resume and paste a job description.")
            return

        resume_text = extract_text_from_pdf(uploaded_file)
        jd_text = job_description

        score, matched_keywords, missing_keywords = calculate_match(resume_text, jd_text)

        st.metric("Match Score (%)", f"{score}")
        st.success("✅ Analysis Complete")

        st.markdown("**Matched Keywords**")
        st.write(", ".join(list(matched_keywords)[:30]) or "None")

        st.markdown("**Missing Keywords**")
        st.write(", ".join(list(missing_keywords)[:30]) or "None")

        save_resume_result(user_id, resume_text, jd_text, score)
        st.success("✔️ Result Saved to Your Profile")
