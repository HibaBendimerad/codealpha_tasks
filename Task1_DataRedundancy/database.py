import sqlite3

def create_database():
    """Creates the cloud database and the employees table"""
    conn = sqlite3.connect("cloud_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            date_added TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Cloud database initialized successfully!")