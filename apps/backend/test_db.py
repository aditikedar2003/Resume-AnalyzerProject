import psycopg2
import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Database config from .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # Create users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            role VARCHAR(50)
        );
    """)

    # Create resumes table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            resume_id SERIAL PRIMARY KEY,
            file_name VARCHAR(255),
            file_data BYTEA,
            user_id INTEGER REFERENCES users(user_id)
        );
    """)

    # Create job_descriptions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            jd_id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            user_id INTEGER REFERENCES users(user_id)
        );
    """)

    # Create cover_letters table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cover_letters (
            cover_id SERIAL PRIMARY KEY,
            filename VARCHAR(255),
            user_id INTEGER REFERENCES users(user_id)
        );
    """)

    # Create linkedin_profiles table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS linkedin_profiles (
            profile_id SERIAL PRIMARY KEY,
            summary TEXT,
            job_description TEXT,
            user_id INTEGER REFERENCES users(user_id)
        );
    """)

    # Create job_tracker table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_tracker (
            tracker_id SERIAL PRIMARY KEY,
            company_name VARCHAR(255),
            position VARCHAR(255),
            status VARCHAR(50),
            notes TEXT,
            user_id INTEGER REFERENCES users(user_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All tables created successfully!")

except Exception as e:
    print("❌ Error:", e)
