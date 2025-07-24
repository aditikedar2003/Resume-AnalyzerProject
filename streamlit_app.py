import streamlit as st
from views.auth import show_login_page, show_signup_page

st.set_page_config(page_title="JobBoost - Resume Analyzer", layout="wide")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if st.session_state.logged_in:
        st.title("Welcome to JobBoost 🎯")
        st.success("You are logged in.")
        st.write("🔍 Navigate to the Resume Scanner, Cover Letter Analyzer, etc.")
    else:
        if st.session_state.page == 'login':
            show_login_page()
        elif st.session_state.page == 'signup':
            show_signup_page()

if __name__ == "__main__":
    main()
