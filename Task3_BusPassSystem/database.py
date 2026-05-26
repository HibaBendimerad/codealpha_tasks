import sqlite3

def create_database():
    """Creates the cloud bus pass database"""
    conn = sqlite3.connect("bus_pass.db")
    cursor = conn.cursor()

    # Routes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            price REAL NOT NULL,
            available_seats INTEGER NOT NULL
        )
    """)

    # Tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_number TEXT NOT NULL UNIQUE,
            passenger_name TEXT NOT NULL,
            passenger_email TEXT NOT NULL,
            route_id INTEGER NOT NULL,
            seat_number INTEGER NOT NULL,
            booking_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'CONFIRMED',
            FOREIGN KEY (route_id) REFERENCES routes(id)
        )
    """)

    # Insert sample routes if empty
    cursor.execute("SELECT COUNT(*) FROM routes")
    if cursor.fetchone()[0] == 0:
        routes = [
            ("Oran",        "Algiers",     "06:00", "10:30", 850.00, 40),
            ("Algiers",     "Oran",        "07:00", "11:30", 850.00, 40),
            ("Oran",        "Constantine", "08:00", "14:00", 1200.00, 35),
            ("Constantine", "Oran",        "09:00", "15:00", 1200.00, 35),
            ("Algiers",     "Annaba",      "06:30", "11:00", 1100.00, 40),
            ("Annaba",      "Algiers",     "07:30", "12:00", 1100.00, 40),
            ("Oran",        "Tlemcen",     "10:00", "12:00", 450.00,  30),
            ("Tlemcen",     "Oran",        "11:00", "13:00", 450.00,  30),
        ]
        cursor.executemany("""
            INSERT INTO routes (origin, destination, departure_time, arrival_time, price, available_seats)
            VALUES (?, ?, ?, ?, ?, ?)
        """, routes)

    conn.commit()
    conn.close()