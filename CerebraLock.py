import os
from cryptography.fernet import Fernet

# Function to generate a key for encryption if it doesn't exist
def generate_key():
    return Fernet.generate_key()

# Function to load the encryption key from the file
def load_key():
    if os.path.exists("config.dat"):
        with open("config.dat", "rb") as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open("config.dat", "wb") as key_file:
            key_file.write(key)
        return key

# Function to encrypt a password
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted

# Function to decrypt a password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password).decode()
    return decrypted

# Function to save a service and encrypted password
def save_password(service, username, encrypted_password):
    with open("storage.dat", "ab") as password_file:
        password_file.write(service.encode() + b":" + username.encode() + b":" + encrypted_password + b"\n")

# Function to load and decrypt stored passwords
def load_passwords(key):
    if not os.path.exists("storage.dat"):
        print("No passwords saved yet!")
        return {}

    passwords = {}
    with open("storage.dat", "rb") as password_file:
        lines = password_file.readlines()
        for line in lines:
            service, username, encrypted_password = line.split(b":", 2)
            decrypted_password = decrypt_password(encrypted_password.strip(), key)
            passwords[service.decode()] = (username.decode(), decrypted_password)
    return passwords

def main():
    # Prompt for master password on start
    master_password = input("Enter your master password to continue: ")

    # Set the correct master password here
    correct_master_password = "super_secret_password_here"

    if master_password != correct_master_password:
        print("Incorrect password! Access denied.")
        return

    print("Access granted!")

    # Load the encryption key
    key = load_key()

    while True:
        print("\nPassword Manager Menu")
        print("1. View a password")
        print("2. Add a password")
        print("3. Remove a password")
        print("4. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            # View a password
            service = input("Enter the service name: ")
            passwords = load_passwords(key)
            if service in passwords:
                username, password = passwords[service]
                print(f"Service: {service}\nUsername: {username}\nPassword: {password}")
            else:
                print(f"No password found for {service}.")

        elif choice == "2":
            # Add a password
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            encrypted_password = encrypt_password(password, key)
            save_password(service, username, encrypted_password)
            print(f"Password for {service} saved!")

        elif choice == "3":
            # Remove a password
            service_to_delete = input("Enter the service name to remove: ")
            passwords = load_passwords(key)
            if service_to_delete in passwords:
                passwords.pop(service_to_delete)
                with open("storage.dat", "wb") as password_file:
                    for svc, (username, password) in passwords.items():
                        encrypted_password = encrypt_password(password, key)
                        password_file.write(svc.encode() + b":" + username.encode() + b":" + encrypted_password + b"\n")
                print(f"Password for {service_to_delete} removed.")
            else:
                print(f"No password found for {service_to_delete}.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
