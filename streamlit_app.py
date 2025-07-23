import streamlit as st
import psycopg2
from dotenv import load_dotenv
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="JobBoost - Resume Analyzer", layout="centered")

# ======= Styling =======
st.markdown("""
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
        }
        .main {
            padding: 2rem;
        }
        .upload-box {
            border: 2px dashed #007BFF;
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .section-header {
            font-size: 28px;
            color: #007BFF;
            font-weight: bold;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📄 JobBoost - Resume vs Job Match")

# ======= Database Connection =======
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)
cursor = conn.cursor()

# ======= Helper Functions =======

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(uploaded_file):
    return docx2txt.process(uploaded_file)

def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(similarity[0][0]) * 100, 2)

# ======= Main UI Section =======
st.markdown("### 1. Upload Your Resume")
uploaded_resume = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])

st.markdown("### 2. Paste Job Description")
job_description = st.text_area("Paste the job description here...", height=200)

if st.button("⚡ Analyze Now"):
    if uploaded_resume and job_description.strip():
        file_name = uploaded_resume.name

        if uploaded_resume.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_resume)
        elif uploaded_resume.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            resume_text = extract_text_from_docx(uploaded_resume)
        else:
            st.error("Unsupported file format.")
            st.stop()

        match_score = calculate_match(resume_text, job_description)

        # Save to database
        cursor.execute(
            "INSERT INTO resumes (file_name, job_description, match_score, created_at) VALUES (%s, %s, %s, %s)",
            (file_name, job_description, match_score, datetime.now())
        )
        conn.commit()

        st.success(f"✅ Match Score: **{match_score}%**")
        st.progress(int(match_score))

    else:
        st.warning("Please upload a resume and paste job description to proceed.")

# ======= Match History =======
st.markdown("### 📊 Match History")

try:
    cursor.execute("SELECT file_name, match_score, created_at FROM resumes ORDER BY created_at DESC LIMIT 10")
    rows = cursor.fetchall()

    if rows:
        st.table([
            {"Resume": row[0], "Match %": f"{row[1]}%", "Date": row[2].strftime("%Y-%m-%d %H:%M")}
            for row in rows
        ])
    else:
        st.info("No history found.")
except Exception as e:
    st.error("⚠️ Error fetching history. Please ensure your database is up-to-date.")
