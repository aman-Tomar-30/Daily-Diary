import hashlib
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet

todays_date = datetime.now().strftime("%d-%m-%Y")

while True:
    # ---------- Verify Password ----------
    def verify_password():
        pwd = getpass("🔐 Enter diary password: ")
        hashed_input = hashlib.sha256(pwd.encode()).hexdigest()

        try:
            with open("password.key", "r") as f:
                stored_hash = f.read()
        except FileNotFoundError:
            print("❌ Password not found. Set password first.")
            return False

        return hashed_input == stored_hash

    # ---------- Get Key ----------
    def load_cipher():
        with open("secret.key", "rb") as f:
            key = f.read()
        return Fernet(key)

    # ---------- Encrypt Text ----------
    def encrypt_text(text):
        cipher = load_cipher()
        return cipher.encrypt(text.encode())

    # ---------- Decrypt Text ----------
    def decrypt_text(data):
        cipher = load_cipher()
        return cipher.decrypt(data).decode()


    # ---------- Formatting Function ----------
    def format_text(text, words_per_line=20):
        words = text.split()
        lines = []

        for i in range(0, len(words), words_per_line):
            line = " ".join(words[i:i + words_per_line])
            lines.append(line)

        return lines
        

    # ---------- Save Diary Entry ----------

    def save_entry_encrypted(text, filename=f"Entries/{todays_date}.txt"):
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y | %H:%M")
        
        content = f"\n📅 Date: {date_time}\n\n{text}\n\n" + "-" * 50 +"END"+"-" * 50+ "\n"
        encrypted = encrypt_text(content)
        
        with open(filename, "ab") as file:
            file.write(encrypted + b"\n")
            
        print("\n ✅ Diary entry saved successfully!")

    # ---------- Read Diary Entry ----------
    def read_diary(filename=f"Entries/{todays_date}.txt"):
        try:
            with open(filename, "rb") as f:
                data = f.read()

            decrypted = decrypt_text(data)
            print("\n📖 Your Diary:\n")
            lines = decrypted.split("\n")
            for line in lines:
                formatted_lines = format_text(line)
                for formatted_line in formatted_lines:
                    print(formatted_line)
                    
        except Exception:
            print("❌ Unable to decrypt diary (wrong key or corrupted file)")


    # ---------------- MAIN ----------------

    if not verify_password():
        print("❌ Access denied")
        exit()

    print("\n1. Write Diary")
    print("2. Read Diary")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        print("\nWrite diary (ENTER twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        entry = " ".join(lines)
        save_entry_encrypted(entry)
        print("💾 Encrypted diary saved!")

    elif choice == "2":
        date = input("Enter date (DD-MM-YYYY) or press ENTER for today: ")
        if date:
            if read_diary(f"Entries/{date}.txt"):
                read_diary(f"Entries/{date}.txt")
            else:
                print("❌ No entry found for this date.")
        else:
            read_diary()
    
    elif choice == "3":
        print("👋 Goodbye!")
        exit()



