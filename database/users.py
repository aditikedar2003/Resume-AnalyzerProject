from utils.db import get_connection

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
    "id": row[0],
    "full_name": row[1],
    "email": row[2],
    "password": row[3]
}

    return None

def create_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error creating user:", e)
        return False
    finally:
        cur.close()
        conn.close()
