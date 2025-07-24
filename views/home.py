import streamlit as st
from utils.session import get_user_id, clear_user_id

def show_home_page():
    user_id = get_user_id()
    if not user_id:
        st.warning("You must log in to view this page.")
        return

    st.markdown("# 🎯 Resume Analyzer Dashboard")

    if st.button("Logout"):
        clear_user_id()
        st.experimental_rerun()

    st.success("Welcome to your Dashboard. Choose a section from the top.")
