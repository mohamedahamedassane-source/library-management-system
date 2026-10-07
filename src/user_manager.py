"""
Module: user_manager.py
Description: Manages administrator and regular user accounts, authentication, 
profile updates, and secure local JSON file persistence.
"""

import json
import os

class UserManager:
    """Handles data storage, verification, and CRUD operations for Admin and Users."""

    def __init__(self, admin_file="data/admin.json", users_file="data/users.json"):
        self.admin_file = admin_file
        self.users_file = users_file

    #--- ADMINISTRATOR MANAGEMENT METHODS ---
    def load_admin(self):
        """Loads the administrator credentials from the admin JSON file."""

        if os.path.exists(self.admin_file):
            try:
                with open(self.admin_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        return None

    def save_admin(self, email, password):
        """Saves or updates the unique administrator credentials into the JSON file."""

        os.makedirs(os.path.dirname(self.admin_file), exist_ok=True)
        with open(self.admin_file, "w", encoding="utf-8") as f:
            json.dump({"email": email, "password": password}, f, indent=4)

    def verify_admin(self, password):
        """Verifies if the provided password matches the administrator's password."""

        admin = self.load_admin()
        if admin and admin["password"] == password:
            return True
        return False

    # --- REGULAR USER MANAGEMENT METHODS ---
    def load_users(self):
        """Loads all registered regular users from the users JSON file."""

        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_users(self, users):
        """Saves the complete list of users to the users JSON file."""

        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def register_user(self, email, password):
        """Registers a new user if the email is not already taken."""

        users = self.load_users()
        for u in users:
            if u["email"] == email:
                print("X Error : this email is already used.")
                return False
        users.append({"email": email, "password": password})
        self.save_users(users)
        print("User account created with success !")
        return True
    
    def verify_user(self, email, password):
        """Validates user credentials against stored records."""

        users = self.load_users()
        for u in users:
            if u["email"] == email and u["password"] == password:
                return True
        return False

    def update_credentials(self, role, identifier, new_email, new_password):
        """ Updates credentials (email/password) for either the administrator or a specific user. """

        if role == "admin":
            self.save_admin(new_email, new_password)
            print("Admin information updated successfully.")
        else:
            users = self.load_users()
            for u in users:
                if u["email"] == identifier:
                    u["email"] = new_email
                    u["password"] = new_password
                    self.save_admin(users)
                    print("User information updated successfully.")
                    return True
        return False

    def list_all_users(self):
        """Displays and returns the list of all registered users (Admin privilege). """

        users = self.load_users()
        if not users:
            print("No user account registered.")
            return []
        print("\n--- LIST OF USERS ---")
        for i, u in enumerate(users, 1):
            print(f"{i}. Email : {u['email']}")
        return users

    def delete_user_by_email(self, email):
        """Deletes a user account by their email address (Admin privilege)."""
        
        users = self.load_users()
        new_users = [u for u in users if u["email"] != email]
        if len(new_users) < len(users):
            self.save_users(new_users)
            print("User deleted successfully.")
            return True
        print("Error : User not found.")
        return False
        