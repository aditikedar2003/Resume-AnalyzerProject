from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        print("✅ Connected to PostgreSQL database!")
        conn.close()
    except Exception as e:
        print("❌ Failed to connect:", str(e))

if __name__ == "__main__":
    test_connection()
