import streamlit as st
from views.auth import show_login_page, show_signup_page

st.set_page_config(page_title="JobBoost - Resume Analyzer", layout="wide")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if st.session_state.logged_in:
        show_home()
    else:
        if st.session_state.page == 'login':
            show_login_page()
        elif st.session_state.page == 'signup':
            show_signup_page()

def show_home():
    st.title(f"Welcome to JobBoost, {st.session_state.get('user_name', 'User')}! 🎯")
    st.success("You're now logged in.")
    st.write("🔍 Start using Resume Scanner, Cover Letter Analyzer, LinkedIn Optimizer, etc.")

if __name__ == "__main__":
    main()
