import logging
import sys
import os


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.presentation.admin_menu_runner import AdminMenuRunner
from src.presentation.employee_menu_runner import EmployeeMenuRunner
from src.presentation.chef_menu_runner import ChefMenuRunner
from src.common.input_validation import InputValidator

class UserAuthentication:
    def __init__(self):
        self.input_validator = InputValidator()

    def login(self):
        try:
            employee_id = self.input_validator.get_valid_item_id("Enter employee ID: ")
            password = self.input_validator.get_valid_input("Enter password: ")

            request = f"AUTH {employee_id} {password}"
            response = send_request(request)
            print(response)

            if response.startswith("Authenticated as admin"):
                admin_menu_runner = AdminMenuRunner()
                admin_menu_runner.run()
            elif response.startswith("Authenticated as employee"):
                employee_menu_runner = EmployeeMenuRunner()
                employee_menu_runner.run(employee_id)
            elif response.startswith("Authenticated as chef"):
                chef_menu_runner = ChefMenuRunner()
                chef_menu_runner.run(employee_id)
            else:
                print("Authentication failed. Please try again.")
        except Exception as e:
            logging.error(f"Error during login: {e}")
            print("An error occurred during login. Please try again.")

if __name__ == "__main__":
    auth = UserAuthentication()
    auth.login()
