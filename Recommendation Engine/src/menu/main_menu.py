import sys
import os
import datetime
import mysql.connector

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.user import User
from .admin_menu import AdminMenu
from .chef_menu import ChefMenu
from .employee_menu import EmployeeMenu
from src.services.reset_service import ResetService
from src.services.recommendation_service import RecommendationService
from src.models.recommendations import Recommendation

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
        global current_date
        current_date = datetime.date.today()

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
            if role == 'admin':
                MainMenu.admin_menu(employee_id)
            elif role == 'chef':
                MainMenu.chef_menu(employee_id)
            elif role == 'employee':
                MainMenu.employee_menu(employee_id)
        else:
            print("Authentication failed. Please try again.")
        return True

    @staticmethod
    def register():
        employee_id = input("Enter employee ID: ")
        name = input("Enter name: ")
        password = input("Enter password: ")
        role_input = input("Enter role (1.admin, 2.chef, 3.employee): ")
        
        roles = {'1': 'admin', '2': 'chef', '3': 'employee'}
        role = roles.get(role_input)
        
        if not role:
            print("Invalid role. Please enter 1 for admin, 2 for chef, or 3 for employee.")
            return True

        if not employee_id or not name or not password:
            print("Please enter all the information")
            return True

        user = User(employee_id, name, password, role)
        try:
            user.register()
            print("Registration successful.")
        except mysql.connector.Error as err:
            if err.errno == 1062:  
                print(f"Error: Duplicate entry for employee ID '{employee_id}'. Please try again with a different ID.")
            else:
                print(f"Error: {err}")
        return True

    @staticmethod
    def next_day():
        MainMenu.current_date += datetime.timedelta(days=1)
        if ResetService.reset_daily_data():
            RecommendationService.check_discard_criteria()
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
    def admin_menu(employee_id):
        while True:
            AdminMenu.display()
            choice = input("Enter choice: ")
            if not AdminMenu.handle_choice(choice, employee_id):
                break

    @staticmethod
    def chef_menu(employee_id):
        while True:
            ChefMenu.display()
            choice = input("Enter choice: ")
            if not ChefMenu.handle_choice(choice, employee_id):
                break

    @staticmethod
    def employee_menu(employee_id):
        while True:
            EmployeeMenu.display()
            choice = input("Enter choice: ")
            if not EmployeeMenu.handle_choice(employee_id, choice, MainMenu.first_day, MainMenu.current_date):
                break
    