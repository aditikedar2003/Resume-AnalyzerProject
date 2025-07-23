import streamlit as st
import psycopg2
import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Connect to PostgreSQL database
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Calculate match rate and extract keywords
def calculate_match(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform([resume_text, jd_text])
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = cosine_sim * 100

    resume_tokens = set(resume_text.lower().split())
    jd_tokens = set(jd_text.lower().split())
    matched_keywords = sorted(resume_tokens & jd_tokens)
    missing_keywords = sorted(jd_tokens - resume_tokens)

    return score, matched_keywords, missing_keywords

# --- Streamlit UI ---
st.set_page_config(page_title="Resume Analyzer Pro", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #f5f7fa;}
        header {visibility: hidden;}
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextArea textarea {
            height: 200px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Resume Analyzer Pro")
st.markdown("Compare your resume with the job description and get actionable insights like Jobscan.")

user_id = 1  # TODO: Replace with session-based user auth

col1, col2 = st.columns(2)
with col1:
    resume = st.file_uploader("📄 Upload Your Resume (PDF only)", type=["pdf"])

with col2:
    jd_text = st.text_area("📝 Paste Job Description")

if st.button("🚀 Analyze Match"):
    if resume and jd_text:
        with st.spinner("Processing..."):
            try:
                resume_text = extract_text_from_pdf(resume)

                conn = connect_db()
                cur = conn.cursor()

                # Save Resume
                cur.execute("""
                    INSERT INTO resumes (user_id, filename, content)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (user_id, resume.name, resume_text))
                resume_id = cur.fetchone()[0]

                # Save JD
                jd_filename = f"JD_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
                cur.execute("""
                    INSERT INTO job_descriptions (user_id, filename, content)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (user_id, jd_filename, jd_text))
                job_id = cur.fetchone()[0]

                # Calculate match
                score, matched_keywords, missing_keywords = calculate_match(resume_text, jd_text)

                # Save match result
                cur.execute("""
                    INSERT INTO match_results (resume_id, job_id, match_percentage, keywords_matched)
                    VALUES (%s, %s, %s, %s)
                """, (resume_id, job_id, score, ', '.join(matched_keywords)))

                conn.commit()
                cur.close()
                conn.close()

                st.success("✅ Resume and JD saved to database.")
                st.metric("🎯 Match Rate", f"{score:.2f}%")

                st.markdown(f"### ✅ Matched Keywords ({len(matched_keywords)})")
                st.write(', '.join(matched_keywords) or "None")

                st.markdown(f"### ❌ Missing Keywords ({len(missing_keywords)})")
                st.write(', '.join(missing_keywords) or "None")

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please upload both Resume and Job Description to analyze.")
