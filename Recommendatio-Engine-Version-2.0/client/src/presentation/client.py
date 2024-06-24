import socket

def send_request(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    client.send(request.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    client.close()
    return response

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

if __name__ == "__main__":
    main_menu()
