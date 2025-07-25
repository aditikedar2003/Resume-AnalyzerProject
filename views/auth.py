# views/auth.py

from utils.security import verify_password

# ... inside show_login_page()

user = get_user_by_email(email)

if user and verify_password(password, user["password"]):
    st.success("Login successful!")
    st.session_state.user_id = user["id"]
    st.session_state.page = "Home"
else:
    st.error("Invalid credentials.")
