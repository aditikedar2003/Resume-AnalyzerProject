import streamlit as st
from views.auth import show_login_page, show_signup_page
from views.home import show_home

def main():
    st.set_page_config(page_title="JobBoost - Resume Analyzer", layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.page = 'login'

    if st.session_state.logged_in:
        show_home()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'signup':
        show_signup_page()

if __name__ == "__main__":
    main()
