import streamlit as st
from utils.session import get_user_id
from utils.db import get_db_connection
import datetime

def analyze_linkedin(linkedin_text):
    feedback = []
    score = 0

    if "summary" in linkedin_text.lower():
        feedback.append("✅ Summary section found.")
        score += 20
    else:
        feedback.append("⚠️ Consider adding a summary section.")

    if "experience" in linkedin_text.lower():
        feedback.append("✅ Experience section included.")
        score += 20
    else:
        feedback.append("⚠️ Include relevant work experience.")

    if "skills" in linkedin_text.lower():
        feedback.append("✅ Skills listed.")
        score += 20
    else:
        feedback.append("⚠️ Add a skills section.")

    if "certification" in linkedin_text.lower() or "license" in linkedin_text.lower():
        feedback.append("✅ Certifications or licenses mentioned.")
        score += 20
    else:
        feedback.append("⚠️ Add certifications or licenses if available.")

    if "education" in linkedin_text.lower():
        feedback.append("✅ Education section present.")
        score += 20
    else:
        feedback.append("⚠️ Include education history.")

    return score, feedback

def show_linkedin_optimizer():
    user_id = get_user_id()
    if not user_id:
        st.warning("Please log in to use the LinkedIn Optimizer.")
        return

    st.header("🔗 LinkedIn Optimizer")

    linkedin_text = st.text_area("Paste your LinkedIn profile content here")

    if st.button("Analyze"):
        if linkedin_text.strip() == "":
            st.error("Please paste your LinkedIn content first.")
        else:
            score, feedback = analyze_linkedin(linkedin_text)
            st.success(f"LinkedIn Profile Score: {score}/100")

            for item in feedback:
                st.write(item)

            # Save to DB
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO linkedin_profiles (user_id, content, score, created_at) VALUES (%s, %s, %s, %s)",
                (user_id, linkedin_text, score, datetime.datetime.now())
            )
            conn.commit()
            conn.close()
            st.info("Saved successfully.")
