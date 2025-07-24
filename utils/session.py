import streamlit as st

def get_user_id():
    return st.session_state.get("user_id")

def set_user_id(user_id):
    st.session_state["user_id"] = user_id

def clear_user_id():
    if "user_id" in st.session_state:
        del st.session_state["user_id"]
