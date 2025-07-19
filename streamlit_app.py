import streamlit as st

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Navigation Header
st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f8f8f8;
        padding: 10px 40px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    .nav-links a {
        margin: 0 15px;
        text-decoration: none;
        font-weight: bold;
        color: #333;
    }
    .nav-links a:hover {
        color: #007BFF;
    }
    </style>
    <div class="navbar">
        <div style="display: flex; align-items: center;">
            <img src="https://raw.githubusercontent.com/aditikedar2003/resume-analyzer-frontend/main/public/logo.png" width="50" style="margin-right: 10px;" />
            <h2 style="margin: 0;">Resume Analyzer</h2>
        </div>
        <div class="nav-links">
            <a href="#Home">Home</a>
            <a href="#Resume-Scanner">Resume Scanner</a>
            <a href="#Cover-Letter">Cover Letter</a>
            <a href="#LinkedIn">LinkedIn</a>
            <a href="#Job-Tracker">Job Tracker</a>
            <a href="#Login">Login</a>
            <a href="#Signup">Sign Up</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Center Logo
st.markdown("""
    <div style='text-align:center; margin-top: 40px;'>
        <img src='https://raw.githubusercontent.com/aditikedar2003/resume-analyzer-frontend/main/public/logo.png' width='120'/>
        <h1>Resume Analyzer</h1>
    </div>
""", unsafe_allow_html=True)

# You can continue to build out Resume Scanner, Cover Letter, LinkedIn, Job Tracker here...
