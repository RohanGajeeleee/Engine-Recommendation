import sys
import os
import datetime

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary modules and services
from src.models.user import User
from .admin_menu import AdminMenu
from .chef_menu import ChefMenu
from .employee_menu import EmployeeMenu
from src.services.reset_service import ResetService

class MainMenu:
    MENU_CHOICES = {
        'LOGIN': '1',
        'REGISTER': '2',
        'NEXT_DAY': '3',
        'EXIT': '4'
    }

    first_day = True
    current_date = datetime.date.today()

    @staticmethod
    def display():
        print("\nMain Menu")
        print("1. Login")
        print("2. Register")
        print("3. Next Day")
        print("4. Exit")

    @staticmethod
    def run():
        actions = {
            MainMenu.MENU_CHOICES['LOGIN']: MainMenu.login,
            MainMenu.MENU_CHOICES['REGISTER']: MainMenu.register,
            MainMenu.MENU_CHOICES['NEXT_DAY']: MainMenu.next_day,
            MainMenu.MENU_CHOICES['EXIT']: MainMenu.exit_program
        }

        while True:
            MainMenu.display()
            choice = input("Enter choice: ")
            action = actions.get(choice, MainMenu.invalid_choice)
            if not action():
                break

    @staticmethod
    def login():
        employee_id = input("Enter employee ID: ")
        password = input("Enter password: ")
        role = User.authenticate(employee_id, password)
        if role:
            print(f"Authenticated as {role}")
            MainMenu.navigate_role_menu(role, employee_id)
        else:
            print("Authentication failed. Please try again.")
        return True

    @staticmethod
    def navigate_role_menu(role, employee_id):
        if role == 'admin':
            MainMenu.admin_menu()
        elif role == 'chef':
            MainMenu.chef_menu()
        elif role == 'employee':
            MainMenu.employee_menu(employee_id)

    @staticmethod
    def register():
        employee_id = input("Enter employee ID: ")
        name = input("Enter name: ")
        password = input("Enter password: ")
        role = input("Enter role (admin, chef, employee): ")
        user = User(employee_id, name, password, role)
        user.register()
        return True

    @staticmethod
    def next_day():
        MainMenu.current_date += datetime.timedelta(days=1)
        if ResetService.reset_daily_data():
            MainMenu.first_day = False
            print(f"Simulated date: {MainMenu.current_date}")
            print("Chef needs to log in and generate food recommendations for the next day.")
        else:
            print("Chef needs to choose items for the next day before transitioning.")
        return True

    @staticmethod
    def exit_program():
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True

    @staticmethod
    def admin_menu():
        while True:
            AdminMenu.display()
            choice = input("Enter choice: ")
            if not AdminMenu.handle_choice(choice):
                break

    @staticmethod
    def chef_menu():
        while True:
            ChefMenu.display()
            choice = input("Enter choice: ")
            if not ChefMenu.handle_choice(choice):
                break

    @staticmethod
    def employee_menu(employee_id):
        while True:
            EmployeeMenu.display()
            choice = input("Enter choice: ")
            if not EmployeeMenu.handle_choice(employee_id, choice, MainMenu.first_day, MainMenu.current_date):
                break
