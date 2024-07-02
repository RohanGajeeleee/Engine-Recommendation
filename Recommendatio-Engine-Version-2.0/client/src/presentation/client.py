import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
import logging
from common.network_utils import send_request
from common.input_validation import InputValidator

logging.basicConfig(level=logging.INFO)


class MainMenu:
    @staticmethod
    def display():
        while True:
            print("\nMain Menu")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                UserRegistration.register()
            elif choice == '2':
                UserAuthentication.login()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

class UserRegistration:
    @staticmethod
    def register():
        try:
            employee_id = InputValidator.get_valid_item_id("Enter employee ID: ")
            name = InputValidator.get_valid_input("Enter name: ")
            password = InputValidator.get_valid_input("Enter password: ")
            role = InputValidator.get_valid_role("Enter role (admin, chef, employee): ")

            if role == 'employee':
                dietary_preference = InputValidator.get_valid_dietary_type("Enter dietary preference (1 for Vegetarian, 2 for Non-Vegetarian, 3 for Eggetarian): ")
                spice_level = InputValidator.get_valid_spice_level("Enter spice level (1 for Low, 2 for Medium, 3 for High): ")
                cuisine_preference = InputValidator.get_valid_food_category("Enter cuisine preference (1 for North Indian, 2 for South Indian, 3 for Other): ")
                sweet_tooth = InputValidator.get_valid_sweet_tooth("Do you have a sweet tooth? (1 for Yes, 2 for No): ")

                profile_details = f"{dietary_preference} {spice_level} {cuisine_preference} {sweet_tooth}"
            else:
                profile_details = ""

            request = f"REGISTER {employee_id} {name} {password} {role} {profile_details}"
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            print("An error occurred during registration. Please try again.")

class UserAuthentication:
    @staticmethod
    def login():
        try:
            employee_id = input("Enter employee ID: ")
            password = input("Enter password: ")

            request = f"AUTH {employee_id} {password}"
            response = send_request(request)
            print(response)
            if response.startswith("Authenticated as admin"):
                AdminMenuRunner.run()
            elif response.startswith("Authenticated as employee"):
                EmployeeMenuRunner.run(employee_id)
            elif response.startswith("Authenticated as chef"):
                ChefMenuRunner.run(employee_id)
        except Exception as e:
            logging.error(f"Error during login: {e}")
            print("An error occurred during login. Please try again.")

class AdminMenuRunner:
    @staticmethod
    def run():
        from presentation.admin_menu import AdminMenu
        while True:
            AdminMenu.display()
            choice = input("Enter choice: ")
            if not AdminMenu.handle_choice(choice):
                break

class EmployeeMenuRunner:
    @staticmethod
    def run(employee_id):
        from presentation.employee_menu import EmployeeMenu
        from datetime import datetime
        first_day = False  
        current_date = datetime.now().date()
        while True:
            EmployeeMenu.display()
            choice = input("Enter choice: ")
            if not EmployeeMenu.handle_choice(employee_id, choice, first_day, current_date):
                break

class ChefMenuRunner:
    @staticmethod
    def run(chef_id):
        from presentation.chef_menu import ChefMenu
        while True:
            ChefMenu.display()
            choice = input("Enter choice: ")
            if not ChefMenu.handle_choice(chef_id, choice):
                break

if __name__ == "__main__":
    MainMenu.display()
