import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Database connection

def connect_db():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
    except Exception as e:
        st.error("❌ DB Connection Error: " + str(e))
        return None

# Extract text from PDF

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Match resume vs JD using TF-IDF + cosine similarity

def analyze_match(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_percentage = round(match_score * 100, 2)

    resume_tokens = set(tfidf.inverse_transform(tfidf_matrix[0])[0])
    jd_tokens = set(tfidf.inverse_transform(tfidf_matrix[1])[0])
    matched_keywords = list(resume_tokens.intersection(jd_tokens))
    missing_keywords = list(jd_tokens - resume_tokens)

    return match_percentage, matched_keywords, missing_keywords

# Header navigation
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("https://raw.githubusercontent.com/aditikedar2003/Resume-AnalyzerProject/main/logo.png", width=100)
with col2:
    st.markdown("""
    <style>
    .header-nav {
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
    }
    .header-nav a {
        color: black;
        text-decoration: none;
        font-weight: bold;
    }
    .header-nav a:hover {
        color: #FF4B4B;
    }
    </style>
    <div class='header-nav'>
        <a href='/?app_mode=Home'>Home</a>
        <a href='/?app_mode=Resume Scanner'>Resume Scanner</a>
        <a href='/?app_mode=Cover Letter Scanner'>Cover Letter</a>
        <a href='/?app_mode=LinkedIn Optimizer'>LinkedIn</a>
        <a href='/?app_mode=Job Tracker'>Job Tracker</a>
        <a href='/?app_mode=Login'>Login</a>
        <a href='/?app_mode=Signup'>Sign Up</a>
    </div><br><br>
    """, unsafe_allow_html=True)

app_mode = st.query_params.get("app_mode", "Home")

# Pages
if app_mode == "Home":
    st.markdown("<h1 style='text-align: center;'>Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("""
        ## Features:
        - ✅ ATS Resume Scanner
        - ✅ Cover Letter Analyzer
        - ✅ LinkedIn Optimizer
        - ✅ Job Tracker
        
        Upload your resume, match it with job descriptions and optimize everything from one platform!
    """)

elif app_mode == "Resume Scanner":
    st.header("📄 Upload Your Resume & Job Description")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):
        if resume_file and jd_text:
            resume_text = extract_text_from_pdf(resume_file)
            match_rate, matched_keywords, missing_keywords = analyze_match(resume_text, jd_text)

            conn = connect_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO resumes (filename, content) VALUES (%s, %s)", (resume_file.name, jd_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Resume and JD saved to database.")

            st.subheader(f"🎯 Match Rate: {match_rate}%")
            st.markdown(f"**✅ Matched Keywords:** {matched_keywords}")
            st.markdown(f"**❌ Missing Keywords:** {missing_keywords}")
        else:
            st.warning("Please upload resume and enter JD.")

# Other pages remain unchanged...
# (You can copy them over or let me help enhance them next.)

st.markdown("---")
st.markdown("Built with ❤️ by Aditi Kedar · Powered by Streamlit")
