import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime

load_dotenv()

# --- DB CONNECTION ---
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

# --- TEXT EXTRACTION ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() or ''
    return text

# --- MATCHING LOGIC ---
def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)

    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched_keywords = list(jd_words & resume_words)
    missing_keywords = list(jd_words - resume_words)

    return score, matched_keywords, missing_keywords

# --- MAIN UI ---
st.set_page_config("Resume Analyzer Pro", layout="centered")
st.title("🧠 Resume Analyzer Pro")
st.subheader("Match Your Resume to a Job Description Like Jobscan")

# --- UPLOAD SECTION ---
resume = st.file_uploader("📄 Upload your Resume (PDF only)", type=['pdf'])
jd = st.text_area("📝 Paste Job Description here")

if st.button("Analyze Match") and resume and jd:
    resume_text = extract_text_from_pdf(resume)
    jd_text = jd

    score, matched_keywords, missing_keywords = calculate_match(resume_text, jd_text)

    # --- DB SAVE ---
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Save resume and JD
        cur.execute("INSERT INTO resumes (filename, content) VALUES (%s, %s) RETURNING id;",
                    (resume.name, resume_text))
        resume_id = cur.fetchone()[0]

        cur.execute("INSERT INTO job_descriptions (filename, content) VALUES (%s, %s) RETURNING id;",
                    ("Job_Description", jd_text))
        jd_id = cur.fetchone()[0]

        cur.execute("INSERT INTO match_results (resume_id, job_id, match_percentage, keywords_matched) VALUES (%s, %s, %s, %s);",
                    (resume_id, jd_id, score, ', '.join(matched_keywords)))

        conn.commit()
        cur.close()
        conn.close()

        st.success("✅ Resume and JD saved to database.")

    except Exception as e:
        st.error(f"❌ Database error: {e}")

    # --- DISPLAY RESULTS ---
    st.metric("🎯 Match Rate", f"{score:.2f}%")
    st.markdown(f"✅ **Matched Keywords** ({len(matched_keywords)}):")
    st.write(', '.join(matched_keywords))

    st.markdown(f"❌ **Missing Keywords** ({len(missing_keywords)}):")
    st.write(', '.join(missing_keywords))
