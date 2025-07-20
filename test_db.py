from app.db.database import get_sync_db_session

with get_sync_db_session() as db:
    result = db.execute("SELECT 1;")
    print("✅ Connection successful:", result.fetchone())
