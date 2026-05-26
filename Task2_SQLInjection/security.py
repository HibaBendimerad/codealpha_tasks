import sqlite3
import re
from encryption import encrypt_data, decrypt_data, hash_password

# SQL Injection patterns to detect
SQL_INJECTION_PATTERNS = [
    r"(--)",           # SQL comment
    r"(;)",            # Statement terminator
    r"(\bOR\b)",       # OR operator
    r"(\bAND\b)",      # AND operator
    r"(\')",           # Single quote
    r"(\bDROP\b)",     # DROP command
    r"(\bDELETE\b)",   # DELETE command
    r"(\bINSERT\b)",   # INSERT command
    r"(\bUPDATE\b)",   # UPDATE command
    r"(\bSELECT\b)",   # SELECT command
    r"(\bUNION\b)",    # UNION command
    r"(1=1)",          # Always-true condition
    r"(\bEXEC\b)",     # EXEC command
]

def detect_sql_injection(user_input):
    """
    LAYER 1 — Detects SQL injection patterns in user input
    Returns: (is_attack, attack_type)
    """
    input_upper = user_input.upper()
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, input_upper, re.IGNORECASE):
            return True, pattern.replace(r"\b", "").replace("(", "").replace(")", "")
    return False, None

def log_attack(attempted_input, attack_type, status):
    """Logs detected attack attempts into the database"""
    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attack_logs (attempted_input, attack_type, status)
        VALUES (?, ?, ?)
    """, (attempted_input, attack_type, status))
    conn.commit()
    conn.close()

def secure_register(username, password, email, phone, role="user"):
    """
    LAYER 2 — Registers a user with full security:
    - SQL Injection detection on all inputs
    - AES-256 encryption on sensitive data
    - SHA-256 password hashing
    - Parameterized queries (no raw SQL)
    """
    print(f"\n🔐 Attempting to register: '{username}'")

    # --- LAYER 1: SQL Injection Detection ---
    for field_name, field_value in [("username", username), ("email", email), ("phone", phone)]:
        is_attack, attack_type = detect_sql_injection(field_value)
        if is_attack:
            log_attack(field_value, attack_type, "BLOCKED")
            print(f"🚨 SQL INJECTION DETECTED in '{field_name}' field!")
            print(f"   Attack pattern : {attack_type}")
            print(f"   Status         : BLOCKED & LOGGED ❌")
            return False

    # --- LAYER 2: Encrypt sensitive data + Parameterized query ---
    hashed_password  = hash_password(password)
    encrypted_email  = encrypt_data(email)
    encrypted_phone  = encrypt_data(phone)

    try:
        conn = sqlite3.connect("secure_cloud.db")
        cursor = conn.cursor()
        # Parameterized query — safe from SQL injection
        cursor.execute("""
            INSERT INTO users (username, password_hash, email_encrypted, phone_encrypted, role)
            VALUES (?, ?, ?, ?, ?)
        """, (username, hashed_password, encrypted_email, encrypted_phone, role))
        conn.commit()
        conn.close()
        print(f"   Status : REGISTERED SUCCESSFULLY ✅")
        return True
    except sqlite3.IntegrityError:
        print(f"   Status : USERNAME ALREADY EXISTS ❌")
        return False

def secure_login(username, password):
    """Verifies login credentials securely"""
    is_attack, attack_type = detect_sql_injection(username)
    if is_attack:
        log_attack(username, attack_type, "LOGIN BLOCKED")
        print(f"🚨 SQL INJECTION DETECTED during login → BLOCKED ❌")
        return False

    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("""
        SELECT * FROM users WHERE username = ? AND password_hash = ?
    """, (username, hashed))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"✅ Login successful! Welcome, {username}!")
        return True
    else:
        print(f"❌ Invalid credentials for '{username}'")
        return False

def show_all_users():
    """Displays all registered users with decrypted data"""
    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    print("\n" + "="*70)
    print("       👥 SECURE CLOUD DATABASE — REGISTERED USERS")
    print("="*70)
    for user in users:
        print(f"  🔹 ID       : {user[0]}")
        print(f"     Username : {user[1]}")
        print(f"     Password : [SHA-256 HASHED] {user[2][:30]}...")
        print(f"     Email    : {decrypt_data(user[3])}")
        print(f"     Phone    : {decrypt_data(user[4])}")
        print(f"     Role     : {user[5]}")
        print(f"     Joined   : {user[6]}")
        print("-"*70)
    print()

def show_attack_logs():
    """Displays all logged attack attempts"""
    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attack_logs")
    logs = cursor.fetchall()
    conn.close()

    print("\n" + "="*70)
    print("       🚨 ATTACK LOGS — DETECTED SQL INJECTION ATTEMPTS")
    print("="*70)
    if not logs:
        print("   No attacks detected.")
    for log in logs:
        print(f"  ⚠️  ID        : {log[0]}")
        print(f"     Input     : {log[1]}")
        print(f"     Pattern   : {log[2]}")
        print(f"     Status    : {log[3]}")
        print(f"     Timestamp : {log[4]}")
        print("-"*70)
    print()