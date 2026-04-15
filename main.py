from cryptography.fernet import Fernet
import os
import json
import base64
import hashlib
import getpass

DATA_FILE = "passwords.json"


def generate_key(master_password: str) -> bytes:
    hashed = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


def load_or_create_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump({}, file)


def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_password(cipher):
    website = input("Enter website/app name: ")
    username = input("Enter username/email: ")
    password = getpass.getpass("Enter password: ")

    encrypted_password = cipher.encrypt(password.encode()).decode()

    data = load_data()
    data[website] = {
        "username": username,
        "password": encrypted_password
    }
    save_data(data)
    print("Password saved successfully.\n")


def view_passwords(cipher):
    data = load_data()

    if not data:
        print("No saved passwords found.\n")
        return

    for website, details in data.items():
        decrypted_password = cipher.decrypt(details["password"].encode()).decode()
        print(f"Website/App: {website}")
        print(f"Username: {details['username']}")
        print(f"Password: {decrypted_password}")
        print("-" * 30)
import random
import string
def generate_password():
    length = int(input("Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    print(f"Generated Password: {password}\n")

    def delete_password():
         website = input("Enter website/app name to delete: ")
    data = load_data()

    if website in data:
        del data[website]
        save_data(data)
        print("Password deleted successfully.\n")
    else:
        print("Website/App not found.\n")

    def search_password(cipher):
         website = input("Enter website/app name to search: ")
    data = load_data()

    if website in data:
        details = data[website]
        decrypted_password = cipher.decrypt(details["password"].encode()).decode()
        print(f"Website/App: {website}")
        print(f"Username: {details['username']}")
        print(f"Password: {decrypted_password}")
        print("-" * 30)
    else:
        print("Website/App not found.\n") 

def main():
    print("=== Password Manager ===")
    master_password = getpass.getpass("Enter master password: ")

    key = generate_key(master_password)
    cipher = Fernet(key)

    load_or_create_data()

    while True:
        print("\n1. Add Password")
        print("2. View Passwords")
        print("3. Exit")
        print("4. Generate Strong Password")
        print("5. Delete Password")
        print("6. Search Password")

        choice = input("Choose an option: ")

        if choice == "1":
            add_password(cipher)
        elif choice == "2":
            try:
                view_passwords(cipher)
            except Exception:
                print("Incorrect master password or corrupted data.\n")
        elif choice == "3":
            print("Goodbye.")
            break
        elif choice == "4":
                generate_password()
        elif choice == "5":
                delete_password()
        elif choice == "6":
                search_password(cipher)
        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()