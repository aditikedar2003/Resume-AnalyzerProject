# views/navbar.py

import streamlit as st

def show_navbar():
    st.markdown("""
        <style>
            .nav-link {
                padding: 8px 15px;
                margin-right: 10px;
                background-color: #6A0DAD;
                color: white;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 1, 1, 1, 1, 1])
    with cols[0]:
        if st.button("Dashboard"):
            st.session_state["page"] = "dashboard"
            st.experimental_rerun()
    with cols[1]:
        if st.button("Resume"):
            st.session_state["page"] = "resume_scanner"
            st.experimental_rerun()
    with cols[2]:
        if st.button("Cover Letter"):
            st.session_state["page"] = "cover_letter"
            st.experimental_rerun()
    with cols[3]:
        if st.button("LinkedIn"):
            st.session_state["page"] = "linkedin"
            st.experimental_rerun()
    with cols[4]:
        if st.button("Job Tracker"):
            st.session_state["page"] = "job_tracker"
            st.experimental_rerun()
    with cols[5]:
        if st.button("Resume Builder"):
            st.session_state["page"] = "resume_builder"
            st.experimental_rerun()
