"""
Module: main.py
Description: Application entry point managing user roles (Admin vs. User), 
authentication workflows, profile credential resets, log out cycles, interactive CLI menus
with clean page/screen transitions and pauses for user readability.
"""

from src.library import Library
from src.user_manager import UserManager
from src.utils import get_non_empty_input, confirm_action, display_header, get_hidden_password


def main():
    """Main application loop managing authentication, roles, and terminal user interface."""

    library = Library()
    user_mgr = UserManager()

    while True:
        # 1. Page de connexion principale
        display_header("LIBRARY MANAGEMENT SYSTEM - LOGIN")
        print("1. Administrator")
        print("2. User")
        print("3. Exit the system")

        role_choice = input("Choose your role (1-3) : ").strip()

        if role_choice == "1":
            # --- ADMINISTRATOR AUTHENTICATION FLOW ---
            admin_data = user_mgr.load_admin()
            if not admin_data:
                display_header("FIRST LAUNCH: CREATE ADMIN ACCOUNT")
                email = get_non_empty_input("Enter the administrator email : ")
                password = get_hidden_password("Enter the administrator password : ")
                user_mgr.save_admin(email, password)
                print("Administrator saved successfully !")
                input("\nPress Enter to continue...") # Pause 1

            # Admin Login
            display_header("ADMINISTRATOR LOGIN")
            password = get_hidden_password("Enter your password : ")
            if user_mgr.verify_admin(password):
                print("Logging in successfully !")
                current_user_email = user_mgr.load_admin()["email"]
                role = "admin"
                input("\nPress Enter to access dashboard...")# Pause 2
            else:
                print("Error : Incorrect password.")
                input("\nPress Enter to retry...") # Pause 3
                continue

        elif role_choice == "2":
            # --- USER AUTHENTICATION FLOW ---
            display_header("USER SPACE")
            print("1. Create a new account")
            print("2. Log in with an existed account")
            sub_choice = input("Your choice (1-2) : ").strip()

            if sub_choice == "1":
                display_header("USER REGISTRATION")
                email = get_non_empty_input("New email : ")
                password = get_hidden_password("New password : ")
                if not user_mgr.register_user(email, password):
                    input("\nPress Enter to retry...")  #Pause 4
                    continue
                current_user_email = email
                role = "user"
                input("\nPress Enter to continue...")  # Pause 5

            elif sub_choice == "2":
                users = user_mgr.list_all_users()
                if not users:
                    print("Any account existed. Please create one.")
                    input("\nPress Enter to continue...")  #Pause 6
                    continue

                display_header("USER LOGIN")
                email_choice = get_non_empty_input("Enter your email to log in : ")
                # Check if the email exists in records
                exists = any(u["email"] == email_choice for u in users)
                if not exists:
                    print("Error : this e-mail doesn't exist in the system.")
                    input("\nPress Enter to continue...")  # Pause 7
                    continue

                password = get_hidden_password("Enter your password : ")
                if user_mgr.verify_user(email_choice, password):
                    print("You logged in successfully !")
                    current_user_email = email_choice
                    role = "user"
                    input("\nPress Enter to access your dashboard...")  #Pause
                else:
                    print("Incorrect password.")
                    input("\nPress Enter to retry...")  #Pause
                    continue
            else:
                print("Invalid choice.")
                input("\nPress Enter to continue...")  # Pause 10
                continue
            
        elif role_choice == "3":
            display_header("GOODBYE")
            print("Thank you for using the Library Management System. Goodbye!")
            break

        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")  # Pause 11
            continue

        # --- ROLE-BASED INTERACTIVE MENU LOOP ---
        while True:
            # 2. Affichage dynamique du tableau de bord selon le rôle
            if role == "admin":
                display_header(f"ADMINISTRATOR DASHBOARD - [{current_user_email}]")
            else:
                display_header(f"USER DASHBOARD - [{current_user_email}]")
            
            print("1. Display book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Reset(update) my information(email / password)")

            if role == "admin":
                print("5. [ADMIN] Add a book")
                print("6. [ADMIN] Modify a book")
                print("7. [ADMIN] Delete a book")
                print("8 [ADMIN] Manage users (See / Delete)")
                print("9. Log out (disconnect)")
            else:
                print("5. Log out (disconnect)")

            choice = input("Enter your choice : ").strip()

            if choice == "1":
                display_header("CATALOG - ALL BOOKS")
                library.list_books()
                input("\nPress Enter to return to the menu...") # Pause 12
                
            elif choice == "2":
                display_header("BORROW A BOOK")
                library.list_books()
                print("-"*50)
                isbn = get_non_empty_input("ISBN of book to borrow : ")
                library.borrow_book(isbn)
                input("\nPress Enter to continue...") # Pause 13

            elif choice == "3":
                display_header("RETURN A BOOK")
                isbn = get_non_empty_input("ISBN of book to return : ")
                library.return_book(isbn)
                input("\nPress Enter to continue...") # Pause 14

            elif choice == "4":
                display_header("UPDATE MY ACCOUNT PROFILE")
                new_email = get_non_empty_input("New emil : ")
                new_password = get_hidden_password("New password : ")
                if confirm_action("Do you confirm the modification of your account ?"):
                    user_mgr.update_credentials(role, current_user_email, new_email, new_password)
                    current_user_email = new_email
                input("\nPress Enter to continue...") # Pause 15

            elif choice == "5" and role == "admin":
                display_header("ADMIN: ADD A NEW BOOK")
                title = get_non_empty_input("Title : ")
                author = get_non_empty_input("Author : ")
                isbn = get_non_empty_input("ISBN : ")
                library.add_book(title, author, isbn)
                input("\nPress Enter to continue...") # Pause 16

            elif choice == "6" and role == "admin":
                display_header("ADMIN: UPDATE A BOOK")
                library.list_books()
                print("-"*50)
                isbn = get_non_empty_input("ISBN of book to modify : ")
                new_title = get_non_empty_input("New title : ")
                new_author = get_non_empty_input("New author : ")
                if confirm_action("Are you modifying this book ? "):
                    library.update_book(isbn, new_title, new_author)
                input("\nPress Enter to continue...") # Pause 17

            elif choice == "7" and role == "admin":
                display_header("ADMIN: DELETE A BOOK")
                library.list_books()
                print("-"*50)
                isbn = get_non_empty_input("ISBN of book to delete : ")
                if confirm_action("Are you deleting definitively this book?"):
                    library.delete_book(isbn)
                input("\nPress Enter to continue...") # Pause 18

            elif choice == "8" and role == "admin":
                display_header("ADMIN: USER MANAGEMENT")
                users = user_mgr.list_all_users()
                if users:
                    print("-"*50)
                    del_choice = input("Do you want to delete an user ? (y/n) : ").strip().lower()
                    if del_choice in ['y', 'yes']:
                        target_email = get_non_empty_input("EEnter the user email to delete : ")
                        if confirm_action(f"Are you deleting the account of {target_email} ?"):
                            user_mgr.delete_user_by_email(target_email)
                input("\nPress Enter to continue...") # Pause 19

            elif (choice == "9" and role == "admin") or (choice == "5" and role == "user"):
                if confirm_action("Do you want to disconnect (log out) ?"):
                    print("Logging out successfully (disconnection).Returning to login screen.")
                    input("\nPress Enter to continue...") # Pause 20
                    break # Sort du menu pour revenir au choix du rôle principal
            else:
                print("Error : Invalid choice or unauthorized action for your profile.")
                input("\nPress Enter to continue...") # Pause 21
if __name__ == "__main__":
    main()












            