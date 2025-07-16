import streamlit as st
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide",
    page_icon="📄"
)

# --- LOAD LOGO ---
logo = Image.open("assets/logo.png")  # Make sure to upload this to your GitHub repo

# --- HEADER ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=100)
with col2:
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px;">
            <div style="font-size: 26px; font-weight: bold; color: #003366;">Resume Analyzer</div>
            <div>
                <a href="#" style="margin-right: 25px; color: #003366; text-decoration: none; font-weight: 500;">Dashboard</a>
                <a href="#" style="margin-right: 25px; color: #003366; text-decoration: none; font-weight: 500;">Resume Scanner</a>
                <a href="#" style="margin-right: 25px; color: #003366; text-decoration: none; font-weight: 500;">Cover Letter</a>
                <a href="#" style="margin-right: 25px; color: #003366; text-decoration: none; font-weight: 500;">LinkedIn Optimizer</a>
                <a href="#" style="margin-right: 25px; color: #003366; text-decoration: none; font-weight: 500;">Pricing</a>
                <a href="#" style="margin-right: 15px; color: #003366; text-decoration: none;">Login</a>
                <a href="#" style="background-color: #003366; color: white; padding: 6px 16px; border-radius: 5px; text-decoration: none;">Sign Up</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- HERO SECTION ---
st.markdown("""
    <div style="text-align: center; padding: 40px 0 20px 0;">
        <h1 style="color: #003366; font-size: 48px;">Optimize Your Resume. Get More Interviews.</h1>
        <p style="font-size: 20px; color: #555;">Resume Analyzer helps you tailor your resume, cover letter, and LinkedIn to the job you're applying for.</p>
        <a href="#" style="margin-top: 20px; display: inline-block; background-color: #007BFF; color: white; padding: 14px 28px; border-radius: 5px; font-size: 18px; text-decoration: none;">Try it Now</a>
    </div>
""", unsafe_allow_html=True)

# --- FEATURE SECTION ---
features = [
    ("📝 Resume Scanner", "Analyze and improve your resume for ATS and recruiters."),
    ("📄 Cover Letter Builder", "Generate personalized cover letters that align with job descriptions."),
    ("🔗 LinkedIn Optimizer", "Optimize your LinkedIn profile for better visibility and matching."),
    ("📚 Resume Builder", "Use professional templates to build your resume from scratch.")
]

st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)
cols = st.columns(4)
for col, (title, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
            <div style="background-color: #F9F9F9; border: 1px solid #DDD; border-radius: 10px; padding: 20px; height: 200px;">
                <h3 style="color: #003366;">{title}</h3>
                <p style="color: #555;">{desc}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <hr style="margin-top: 40px;">
    <p style="text-align: center; color: #AAA; font-size: 14px;">© 2025 Resume Analyzer. All rights reserved.</p>
""", unsafe_allow_html=True)

