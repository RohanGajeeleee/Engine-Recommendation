import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime
from src.presentation.employee_menu import EmployeeMenu

class EmployeeMenuRunner:
    def __init__(self):
        self.employee_menu = EmployeeMenu()

    def run(self, employee_id):
        first_day = False  
        current_date = datetime.now().date()  

        while True:
            self.employee_menu.display()
            choice = input("Enter choice: ").strip()
            if not self.employee_menu.handle_choice(employee_id, choice, first_day, current_date):
                break

if __name__ == "__main__":
    employee_id = input("Enter employee ID: ").strip()
    runner = EmployeeMenuRunner()
    runner.run(employee_id)
