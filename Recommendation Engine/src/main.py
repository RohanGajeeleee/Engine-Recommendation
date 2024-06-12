import sys
import os

# Ensure the src directory is in the Python path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.Database.init_db import clear_database, insert_initial_data
from src.menu.main_menu import MainMenu

if __name__ == "__main__":
    clear_database()
    insert_initial_data()
    MainMenu.run()
