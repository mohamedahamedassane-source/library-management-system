"""
Module: utils.py
Description: Centralizes utility functions for secure user input validation, action confirmation dialogues, terminal screen page transitions,
and hidden password
"""
import os
import getpass

def get_hidden_password(prompt: str = "Enter password: "):
    """Prompts the user for a password without echoing characters to the terminal."""

    while True:
        # getpass securely hides characters while typing
        password = getpass.getpass(prompt).strip()
        if password:
            return password
        print("Error: Password cannot be empty. Please try again.")

def clear_screen():
    """Clears the terminal screen to simulate switching to a new page."""
    # 'nt' corresponds to windows (cls); other systems use POSIX (clear)
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title: str):
    """Clears the screen and prints a formatted header banner for a new activity page."""

    clear_screen()
    print("="*50)
    print(f"{title.center(46)}")
    print("="*50)

def get_non_empty_input(prompt): 
    # Prompts the user until they provide a non-empty string input.
    
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("X Error : This field can't be empty. Please try again.")

def confirm_action(prompt):
    # Asks the user for a yes/no confirmation before performing a sensitive action.
    """Ask a confirmation (yes/not)"""
    while True:
        choice = input(f"{prompt} (y/n) : ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'non']:
            return False
        print("X Error : Please answer with 'y' (yes) or 'n' (no).")