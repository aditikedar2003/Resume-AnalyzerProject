import streamlit as st

def is_authenticated():
    return "user_id" in st.session_state and st.session_state["user_id"]

def set_user_id(uid):
    st.session_state["user_id"] = uid

def logout():
    st.session_state.pop("user_id", None)
