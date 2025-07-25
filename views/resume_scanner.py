import streamlit as st
from utils.session import get_user_id
from utils.db import insert_resume
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def show_resume_scanner():
    st.subheader("Resume Scanner")
    user_id = get_user_id()

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    job_description = st.text_area("Paste Job Description")

    if st.button("Scan Resume"):
        if uploaded_file and job_description and user_id:
            resume_text = uploaded_file.read().decode("latin1")
            vectorizer = TfidfVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform([resume_text, job_description])
            score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100
            insert_resume(uploaded_file.name, uploaded_file.getvalue(), job_description, user_id)
            st.success(f"Match Score: {score:.2f}%")
        else:
            st.warning("Please upload resume and paste job description.")
