import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.presentation.user_registration import UserRegistration
from src.presentation.user_authentication import UserAuthentication

class MainMenu:
    def __init__(self):
        self.user_registration = UserRegistration()
        self.user_authentication = UserAuthentication()

    def display(self):
        while True:
            print("Main Menu")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter choice: ").strip()
            if choice == '1':
                self.user_registration.register()
            elif choice == '2':
                self.user_authentication.login()
            elif choice == '3':
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.display()
