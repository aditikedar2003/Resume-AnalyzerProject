# database/users.py

from database.connection import get_db_connection

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"id": result[0], "password": result[1]}
    return None
