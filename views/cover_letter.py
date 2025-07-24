# views/cover_letter.py

import streamlit as st
from utils.db import get_db_connection

def show_cover_letter_analyzer():
    st.title("✉ Cover Letter Analyzer")
    cover_file = st.file_uploader("Upload Cover Letter (PDF/DOCX)", type=["pdf", "docx"])
    if st.button("Analyze Cover Letter"):
        if cover_file:
            conn, cur = get_db_connection()
            cur.execute("INSERT INTO cover_letters (filename, user_id) VALUES (%s, %s)",
                        (cover_file.name, st.session_state["user_id"]))
            conn.commit()
            conn.close()
            st.success("Saved successfully!")
        else:
            st.warning("Please upload a file.")
