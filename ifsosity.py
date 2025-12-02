import json
import os
import random
import string
import time

DB_FILE = "ifsosity_db.json"


# ------------------ DATABASE SYSTEM ------------------
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)


# ------------------ UI HELPERS ------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("""
██╗███████╗███████╗ ██████╗  ██████╗ ██████╗ ██╗████████╗██╗   ██╗
██║██╔════╝██╔════╝██╔════╝ ██╔═══██╗██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
██║███████╗█████╗  ██║  ███╗██║   ██║██████╔╝██║   ██║    ╚████╔╝ 
██║╚════██║██╔══╝  ██║   ██║██║   ██║██╔══██╗██║   ██║     ╚██╔╝  
██║███████║███████╗╚██████╔╝╚██████╔╝██║  ██║██║   ██║      ██║   
╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝  
                 IFSOSITY PASSWORD MANAGER
    """)


# ------------------ PASSWORD GENERATOR ------------------
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%&*?"
    return "".join(random.choice(chars) for _ in range(length))


# ------------------ MAIN FEATURES ------------------
def register(db):
    clear()
    banner()
    print("=== Register ===")
    username = input("Choose a username: ")
    if username in db["users"]:
        print("Username already exists!")
        time.sleep(1.5)
        return

    password = input("Choose a password: ")
    recovery = input("Recovery phrase (used for password reset): ")

    db["users"][username] = {
        "password": password,
        "recovery": recovery,
        "vault": {}
    }

    save_db(db)
    print("Account created successfully!")
    time.sleep(1.5)


def login(db):
    clear()
    banner()
    print("=== Login ===")

    username = input("Username: ")
    password = input("Password: ")

    if username in db["users"] and db["users"][username]["password"] == password:
        print("Login successful!")
        time.sleep(1)
        user_menu(db, username)
    else:
        print("Wrong username or password!")
        time.sleep(1.5)


def reset_password(db):
    clear()
    banner()
    print("=== Reset Password ===")

    username = input("Username: ")
    if username not in db["users"]:
        print("User does not exist!")
        time.sleep(1.5)
        return

    recovery = input("Enter your recovery phrase: ")
    if recovery == db["users"][username]["recovery"]:
        print("Correct! Create a new password.")
        new_pass = input("New password: ")

        db["users"][username]["password"] = new_pass
        save_db(db)
        print("Password reset successfully!")
        time.sleep(1.5)
    else:
        print("Wrong recovery phrase!")
        time.sleep(1.5)


# ------------------ USER'S VAULT ------------------
def user_menu(db, username):
    while True:
        clear()
        banner()
        print(f"Logged in as: {username}")
        print("\n1) Generate Password")
        print("2) Save Password in Vault")
        print("3) View Saved Passwords")
        print("4) Logout\n")

        choice = input("Choose: ")

        if choice == "1":
            length = int(input("Length: "))
            pwd = generate_password(length)
            print(f"\nGenerated Password: {pwd}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            label = input("Label (Example: instagram): ")
            pwd = input("Password to save: ")
            db["users"][username]["vault"][label] = pwd
            save_db(db)
            print("Saved successfully!")
            time.sleep(1.5)

        elif choice == "3":
            print("\n=== Saved Passwords ===")
            vault = db["users"][username]["vault"]
            if not vault:
                print("Vault is empty!")
            else:
                for k, v in vault.items():
                    print(f"{k}: {v}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            break


# ------------------ PROGRAM START ------------------
def main():
    db = load_db()

    while True:
        clear()
        banner()
        print("1) Login")
        print("2) Register")
        print("3) Reset Password")
        print("4) Exit\n")

        choice = input("Choose: ")

        if choice == "1":
            login(db)
        elif choice == "2":
            register(db)
        elif choice == "3":
            reset_password(db)
        elif choice == "4":
            break


main()
