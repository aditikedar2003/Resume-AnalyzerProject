import streamlit as st
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import io

# -- Database connection
conn = psycopg2.connect(
    host=st.secrets["DB_HOST"],
    database=st.secrets["DB_NAME"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASS"],
    port=st.secrets["DB_PORT"]
)
cur = conn.cursor()

# -- Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# -- Keyword extraction function
def extract_keywords(text):
    return set(word.lower() for word in text.split() if word.isalpha())

# --------------------
# 📄 RESUME SCANNER UI
# --------------------
st.header("📄 Resume Scanner")

resume = st.file_uploader("Upload your Resume (PDF only)", type=['pdf'])
job_description = st.text_area("Paste Job Description")

if resume and job_description:
    resume_text = extract_text_from_pdf(resume)
    jd_text = job_description

    # Save to DB
    cur.execute("INSERT INTO resumes (file_name, job_description) VALUES (%s, %s)", 
                (resume.name, jd_text))
    conn.commit()

    # TF-IDF & Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

    # Matched & Missing Keywords
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    matched_keywords = sorted(resume_keywords & jd_keywords)
    missing_keywords = sorted(jd_keywords - resume_keywords)

    # ✅ Display results
    st.success("✅ Resume and JD saved to database.")
    st.metric("🎯 Match Rate", f"{score:.2f}%")

    st.markdown(f"✅ **Matched Keywords** ({len(matched_keywords)}):")
    st.write(', '.join(matched_keywords) if matched_keywords else "None")

    st.markdown(f"❌ **Missing Keywords** ({len(missing_keywords)}):")
    st.write(', '.join(missing_keywords) if missing_keywords else "None")
