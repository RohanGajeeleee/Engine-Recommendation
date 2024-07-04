import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.presentation.chef_menu import ChefMenu

class ChefMenuRunner:
    def __init__(self):
        self.chef_menu = ChefMenu()

    def run(self, chef_id):
        while True:
            self.chef_menu.display()
            choice = input("Enter choice: ").strip()
            if not self.chef_menu.handle_choice(chef_id, choice):
                break

