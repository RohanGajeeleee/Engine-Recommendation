import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.presentation.admin_menu import AdminMenu

class AdminMenuRunner:
    def __init__(self):
        self.admin_menu = AdminMenu()

    def run(self):
        while True:
            self.admin_menu.display()
            choice = input("Enter choice: ")
            if not self.admin_menu.handle_choice(choice):
                break

