from views.auth import show_login_page, show_signup_page
# ...

# Check if user is logged in
user_id = get_user_id()

# Auth Flow
if not user_id:
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    if st.session_state["auth_mode"] == "login":
        show_login_page()
    else:
        show_signup_page()
