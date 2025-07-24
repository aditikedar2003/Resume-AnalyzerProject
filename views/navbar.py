import streamlit as st

def show_navbar(selected):
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: space-around;
            padding: 0.75rem;
            background-color: #f0f2f6;
            border-bottom: 1px solid #ddd;
        }
        .navbar a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        .navbar a.active {
            color: #1a73e8;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    pages = {
        "Dashboard": "🏠 Dashboard",
        "Resume Scanner": "📄 Resume Scanner",
        "Cover Letter": "✉️ Cover Letter",
        "LinkedIn Optimizer": "🔗 LinkedIn",
        "Job Tracker": "🗂️ Job Tracker",
        "Resume Builder": "🛠️ Resume Builder",
        "Logout": "🚪 Logout"
    }

    links = ""
    for page, label in pages.items():
        active_class = "active" if page == selected else ""
        links += f'<a href="/?nav={page}" class="{active_class}">{label}</a>'

    st.markdown(f'<div class="navbar">{links}</div>', unsafe_allow_html=True)
