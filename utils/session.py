import streamlit as st

def set_user_id(user_id):
    st.session_state.user_id = user_id

def get_user_id():
    return st.session_state.get("user_id", None)

def logout_user():
    st.session_state.user_id = None
