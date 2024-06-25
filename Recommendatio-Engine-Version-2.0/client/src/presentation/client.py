import sys
import os

# Adjust the path to include the root directory and presentation directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from common.network_utils import send_request

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def register():
    employee_id = input("Enter employee ID: ")
    name = input("Enter name: ")
    password = input("Enter password: ")
    role = input("Enter role (admin, chef, employee): ")

    request = f"REGISTER {employee_id} {name} {password} {role}"
    response = send_request(request)
    print(response)

def login():
    employee_id = input("Enter employee ID: ")
    password = input("Enter password: ")

    request = f"AUTH {employee_id} {password}"
    response = send_request(request)
    print(response)
    if response.startswith("Authenticated as admin"):
        run_admin_menu()
    elif response.startswith("Authenticated as employee"):
        run_employee_menu(employee_id)
    elif response.startswith("Authenticated as chef"):
        run_chef_menu(employee_id)

    

def run_admin_menu():
    from presentation.admin_menu import AdminMenu
    while True:
        AdminMenu.display()
        choice = input("Enter choice: ")
        if not AdminMenu.handle_choice(choice):
            break

def run_employee_menu(employee_id):
    from presentation.employee_menu import EmployeeMenu
    from datetime import datetime
    first_day = False  # Set to True if it's the first day
    current_date = datetime.now().date()
    while True:
        EmployeeMenu.display()
        choice = input("Enter choice: ")
        if not EmployeeMenu.handle_choice(employee_id, choice, first_day, current_date):
            break
def run_chef_menu(chef_id):
    from presentation.chef_menu import ChefMenu
    while True:
        ChefMenu.display()
        choice = input("Enter choice: ")
        if not ChefMenu.handle_choice(chef_id,choice):
            break

if __name__ == "__main__":
    main_menu()