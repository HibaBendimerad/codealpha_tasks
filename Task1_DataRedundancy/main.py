from database import create_database
from redundancy import add_employee, show_all_employees

def main():
    create_database()
    
    print("\n" + "="*70)
    print("   🚀 CLOUD DATA REDUNDANCY REMOVAL SYSTEM — CodeAlpha Internship")
    print("="*70)
    
    # --- Adding initial employee records ---
    print("\n📥 Adding initial employee records...\n")
    add_employee("Hiba Bendimerad",  "hiba.bendimerad@company.com",  "Telecommunications", "+213 550 123 456", "Oran, Algeria")
    add_employee("Sara Amrani",      "sara.amrani@company.com",      "Computer Science",   "+213 660 234 567", "Algiers, Algeria")
    add_employee("Karim Belhadj",    "karim.belhadj@company.com",    "Network Engineering","+213 770 345 678", "Constantine, Algeria")
    add_employee("Nassim Hadj",      "nassim.hadj@company.com",      "Cybersecurity",      "+213 550 456 789", "Annaba, Algeria")
    add_employee("Lina Meziane",     "lina.meziane@company.com",     "Cloud Infrastructure","+213 660 567 890","Tlemcen, Algeria")
    add_employee("Omar Ferhat",      "omar.ferhat@company.com",      "Data Engineering",   "+213 770 678 901", "Setif, Algeria")

    # --- Display current database ---
    show_all_employees()

    # --- Testing duplicate detection ---
    print("="*70)
    print("   🔍 TESTING DUPLICATE DETECTION SYSTEM")
    print("="*70 + "\n")
    
    add_employee("Hiba Duplicate",   "hiba.bendimerad@company.com",  "Other", "+213 000 000 000", "Unknown")
    add_employee("Sara Copy",        "sara.amrani@company.com",      "Other", "+213 000 000 001", "Unknown")
    add_employee("Karim Again",      "karim.belhadj@company.com",    "Other", "+213 000 000 002", "Unknown")
    add_employee("Yacine Boudiaf",   "yacine.boudiaf@company.com",   "DevOps","+213 550 789 012", "Bejaia, Algeria")

    # --- Display final database ---
    show_all_employees()
    
    print("="*70)
    print("   ✅ SYSTEM VALIDATION COMPLETE — Only unique records stored")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()