import streamlit as st
from utils.session import get_user_id
from utils.db import get_db_connection
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime

def extract_text_from_resume(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    elif uploaded_file.name.endswith('.docx'):
        return docx2txt.process(uploaded_file)
    else:
        return ""

def show_resume_matcher():
    user_id = get_user_id()
    if not user_id:
        st.warning("You must log in to use the Resume Matcher.")
        return

    st.header("📄 Resume Matcher")

    resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"])
    job_description = st.text_area("Paste the Job Description")

    if st.button("Match"):
        if resume_file and job_description:
            resume_text = extract_text_from_resume(resume_file)
            documents = [resume_text, job_description]

            tfidf = TfidfVectorizer()
            tfidf_matrix = tfidf.fit_transform(documents)
            match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            match_percent = round(match_score * 100, 2)

            st.success(f"✅ Match Score: {match_percent}%")

            # Save in DB
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO resumes (user_id, file_name, match_score, created_at) VALUES (%s, %s, %s, %s)",
                (user_id, resume_file.name, match_percent, datetime.datetime.now())
            )
            conn.commit()
            conn.close()
            st.info("Saved successfully.")
        else:
            st.error("Please upload a resume and paste a job description.")
