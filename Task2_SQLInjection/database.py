import sqlite3

def create_database():
    """Creates the secure cloud database"""
    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email_encrypted TEXT NOT NULL,
            phone_encrypted TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            date_registered TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attack_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempted_input TEXT NOT NULL,
            attack_type TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Secure cloud database initialized successfully!")