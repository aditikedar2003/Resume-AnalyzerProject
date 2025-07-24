import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# ----------- USER AUTHENTICATION -----------

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def insert_user(full_name, email, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (full_name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (full_name, email, password_hash))
    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id

# ----------- RESUME SCANNER -----------

def save_resume(user_id, filename, content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resumes (user_id, filename, content)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (user_id, filename, content))
    resume_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return resume_id

def save_job_description(user_id, filename, content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO job_descriptions (user_id, filename, content)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (user_id, filename, content))
    job_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return job_id

def save_match_result(resume_id, job_id, match_percentage, keywords_matched):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO match_results (resume_id, job_id, match_percentage, keywords_matched)
        VALUES (%s, %s, %s, %s)
    """, (resume_id, job_id, match_percentage, keywords_matched))
    conn.commit()
    conn.close()

# ----------- DASHBOARD / PROFILE -----------

def get_user_resumes(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resumes WHERE user_id = %s ORDER BY uploaded_at DESC", (user_id,))
    resumes = cur.fetchall()
    conn.close()
    return resumes

def get_user_job_descriptions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM job_descriptions WHERE user_id = %s ORDER BY uploaded_at DESC", (user_id,))
    jobs = cur.fetchall()
    conn.close()
    return jobs

def get_match_results_for_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.filename AS resume_name, j.filename AS job_name, m.match_percentage, m.keywords_matched
        FROM match_results m
        JOIN resumes r ON m.resume_id = r.id
        JOIN job_descriptions j ON m.job_id = j.id
        WHERE r.user_id = %s
        ORDER BY m.matched_at DESC
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results
