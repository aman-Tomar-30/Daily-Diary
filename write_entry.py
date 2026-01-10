import sqlite3
from getpass import getpass
import hashlib

connection = sqlite3.connect("example.db")
cursor = connection.cursor()
def write_entry(user_id, content):
    cursor.execute(f"INSERT INTO entries (user_id, content) VALUES (?, ?)", (user_id, content))
    connection.commit()
    print("✅ Diary entry saved successfully!")
    
def read_entries(user_id):
    create_date = input("Enter date (YYYY-MM-DD) or press ENTER for all entries: ")
    if create_date:
        cursor.execute(f"SELECT content, created_at FROM entries WHERE user_id = ? AND DATE(created_at) = ?", (user_id, create_date))
    else:
        cursor.execute(f"SELECT content FROM entries WHERE user_id = ?", (user_id,))
    entries = cursor.fetchall()
    #print(entries)
    if entries:
        print("📖 Your Diary Entries:\n")
        for content,created_at in entries:
            print(f"--- {created_at} ---\n")
            print(content)
            print("\n")
    else:
        print("No diary entries found.")

def new_user():
    username = input("Choose a username: ")
    try:
        cursor.execute(f"SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print("❌ Username already exists.")
            return
        password = getpass("Choose a password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(f"INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
        return
    connection.commit()
    print("✅ User created successfully!")
    
def verify_user():
    username = input("Username: ")
    try:
        cursor.execute(f"SELECT id FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            print("❌ Username does not exist.")
            return None         
    except sqlite3.IntegrityError:
        print("❌ Username does not exist.")
        return None
    password = getpass("Password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(f"SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    result = cursor.fetchone()
    if result:
        print("✅ Access granted")
        return result[0]  # return user_id
    else:
        print("❌ Access denied")
        return None
    return None

if __name__ == "__main__":
    print("1. New User")
    print("2. Login")
    choice = input("Choose: ")
    
    if choice == "1":
        new_user()
        exit()
    elif choice == "2":
        user_id = verify_user()
        if not user_id:
            exit()
    else:
        print("Invalid choice")
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
        write_entry(user_id, entry)
        
    elif choice == "2":
        read_entries(user_id)
        
    elif choice == "3":
        exit()
        
    else:
        print("Invalid choice")
