import hashlib
from getpass import getpass

password = getpass("Create diary password: ")
hashed = hashlib.sha256(password.encode()).hexdigest()

with open("password.key", "w") as f:
    f.write(hashed)

print("✅ Password created successfully")
