import sqlite3

def is_duplicate(email):
    """Checks if an email already exists in the database"""
    conn = sqlite3.connect("cloud_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_employee(name, email, department, phone, location):
    """Adds an employee only if no duplicate is detected"""
    if is_duplicate(email):
        print(f"❌ DUPLICATE DETECTED : '{email}' already exists → Entry rejected")
        return False
    
    conn = sqlite3.connect("cloud_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees (name, email, department, phone, location)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, department, phone, location))
    
    conn.commit()
    conn.close()
    print(f"✅ '{name}' successfully added to the database!")
    return True

def show_all_employees():
    """Displays all records stored in the database"""
    conn = sqlite3.connect("cloud_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    
    print("\n" + "="*70)
    print("          📋 CLOUD DATABASE — CURRENT RECORDS")
    print("="*70)
    if not employees:
        print("   (empty)")
    for emp in employees:
        print(f"  🔹 ID: {emp[0]}")
        print(f"     Name       : {emp[1]}")
        print(f"     Email      : {emp[2]}")
        print(f"     Department : {emp[3]}")
        print(f"     Phone      : {emp[4]}")
        print(f"     Location   : {emp[5]}")
        print(f"     Added on   : {emp[6]}")
        print("-"*70)
    print()