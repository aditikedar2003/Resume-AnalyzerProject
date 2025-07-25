import streamlit as st

def get_current_user_id():
    return st.session_state.get("user_id", None)

def set_current_user(user_id, user_name, user_email):
    st.session_state["user_id"] = user_id
    st.session_state["user_name"] = user_name
    st.session_state["user_email"] = user_email

def clear_session():
    for key in ["user_id", "user_name", "user_email"]:
        if key in st.session_state:
            del st.session_state[key]
