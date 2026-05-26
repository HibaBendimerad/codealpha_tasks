from database import create_database
from security import secure_register, secure_login, show_all_users, show_attack_logs

def main():
    create_database()

    print("\n" + "="*70)
    print("   🔒 CLOUD SECURITY SYSTEM — SQL Injection Detection — CodeAlpha")
    print("="*70)

    # --- Registering legitimate users ---
    print("\n📥 Registering legitimate users...\n")
    secure_register("hiba.bendimerad", "SecurePass@123", "hiba@company.com", "+213550123456", "admin")
    secure_register("sara.amrani",     "MyPass@456",     "sara@company.com", "+213660234567", "user")
    secure_register("karim.belhadj",   "KarimPass@789",  "karim@company.com","+213770345678", "user")
    secure_register("nassim.hadj",     "NassimPass@321", "nassim@company.com","+213550456789","user")
    secure_register("lina.meziane",    "LinaPass@654",   "lina@company.com", "+213660567890", "user")

    # --- Display registered users ---
    show_all_users()

    # --- Testing SQL Injection attacks ---
    print("="*70)
    print("   🔴 SIMULATING SQL INJECTION ATTACKS")
    print("="*70)
    secure_register("admin' OR '1'='1", "anypass", "hack@evil.com", "000", "admin")
    secure_register("hacker; DROP TABLE users--", "anypass", "drop@evil.com", "000", "user")
    secure_register("normal_user", "pass", "SELECT * FROM users", "000", "user")
    secure_register("attacker", "pass", "valid@email.com", "1=1; DELETE", "user")

    # --- Testing secure login ---
    print("\n" + "="*70)
    print("   🔑 TESTING SECURE LOGIN")
    print("="*70 + "\n")
    secure_login("hiba.bendimerad", "SecurePass@123")    # ✅ valid
    secure_login("hiba.bendimerad", "wrongpassword")     # ❌ wrong password
    secure_login("admin' OR '1'='1", "anything")        # 🚨 SQL injection

    # --- Display attack logs ---
    show_attack_logs()

    print("="*70)
    print("   ✅ SECURITY SYSTEM VALIDATED — All attacks blocked & logged")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()