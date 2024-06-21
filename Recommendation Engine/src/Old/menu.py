import sys
import os
import datetime

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.user import User
from src.menu_management import MenuItem
from src.feedback import Feedback
from src.notifications import Notification
from src.recommendations import Recommendation
from src.reporting import Report
from src.db_config import get_db_connection

MENU_CHOICES = {
    'ADMIN': {
        'ADD_ITEM': '1',
        'UPDATE_ITEM': '2',
        'DELETE_ITEM': '3',
        'LOGOUT': '4'
    },
    'CHEF': {
        'VIEW_FEEDBACK': '1',
        'GENERATE_REPORT': '2',
        'GENERATE_RECOMMENDATIONS': '3',
        'LOGOUT': '4'
    },
    'EMPLOYEE': {
        'ADD_FEEDBACK': '1',
        'VIEW_FEEDBACK': '2',
        'CHOOSE_RECOMMENDED_ITEM': '3',
        'VIEW_NOTIFICATIONS': '4',
        'LOGOUT': '5'
    },
    'MAIN': {
        'LOGIN': '1',
        'REGISTER': '2',
        'NEXT_DAY': '3',
        'EXIT': '4'
    }
}

def display_admin_menu():
    print("\nAdmin Menu")
    print("1. Add Menu Item")
    print("2. Update Menu Item")
    print("3. Delete Menu Item")
    print("4. Logout")

def display_chef_menu():
    print("\nChef Menu")
    print("1. View Feedback")
    print("2. Generate Monthly Feedback Report")
    print("3. Generate Recommendations")
    print("4. Logout")

def display_employee_menu():
    print("\nEmployee Menu")
    print("1. Add Feedback")
    print("2. View Feedback")
    print("3. Choose Recommended Item")
    print("4. View Notifications")
    print("5. Logout")

def display_main_menu():
    print("\nMain Menu")
    print("1. Login")
    print("2. Register")
    print("3. Next Day")
    print("4. Exit")

def handle_admin_choice(choice):
    if choice == MENU_CHOICES['ADMIN']['ADD_ITEM']:
        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        availability = input("Enter availability (Available/Unavailable): ")
        menu_item = MenuItem(name=name, price=price, availability=availability)
        menu_item.add()
    elif choice == MENU_CHOICES['ADMIN']['UPDATE_ITEM']:
        item_id = int(input("Enter item ID to update: "))
        name = input("Enter new name (or leave blank to keep current): ")
        price = input("Enter new price (or leave blank to keep current): ")
        availability = input("Enter new availability (or leave blank to keep current): ")
        menu_item = MenuItem(item_id=item_id, name=name if name else None, price=float(price) if price else None, availability=availability if availability else None)
        menu_item.update()
    elif choice == MENU_CHOICES['ADMIN']['DELETE_ITEM']:
        item_id = int(input("Enter item ID to delete: "))
        menu_item = MenuItem(item_id=item_id)
        menu_item.delete()
    elif choice == MENU_CHOICES['ADMIN']['LOGOUT']:
        return False
    else:
        print("Invalid choice. Please try again.")
    return True

def handle_chef_choice(choice):
    if choice == MENU_CHOICES['CHEF']['VIEW_FEEDBACK']:
        Feedback.view()
    elif choice == MENU_CHOICES['CHEF']['GENERATE_REPORT']:
        year = int(input("Enter year: "))
        month = int(input("Enter month: "))
        Report.generate_monthly_feedback_report(year, month)
    elif choice == MENU_CHOICES['CHEF']['GENERATE_RECOMMENDATIONS']:
        recommendations = Recommendation.recommend_items_for_next_day()
        recommendation_data = Recommendation.get_recommendation_data(recommendations)
        print("Items recommended for next day.")
        for data in recommendation_data:
            avg_rating = data[1] if data[1] is not None else 0
            feedback_count = data[2] if data[2] is not None else 0
            print(f"Menu Item: {data[0]}, Average Rating: {avg_rating:.2f}, Feedback Count: {feedback_count}")
        sentiments = Recommendation.analyze_feedback_comments()
        for sentiment in sentiments:
            print(f"Menu ID: {sentiment[0]}, Comment: {sentiment[1]}, Sentiment: {sentiment[2]}")
    elif choice == MENU_CHOICES['CHEF']['LOGOUT']:
        return False
    else:
        print("Invalid choice. Please try again.")
    return True

def handle_employee_choice(employee_id, choice):
    if choice == MENU_CHOICES['EMPLOYEE']['ADD_FEEDBACK']:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT c.menu_id, m.name 
            FROM choices c 
            JOIN menu m ON c.menu_id = m.id 
            WHERE c.employee_id = %s AND c.feedback_given = 0
            """
            cursor.execute(query, (employee_id,))
            choices = cursor.fetchall()

            if not choices:
                print("No items available for feedback.")
                return True

            print("Items available for feedback:")
            for choice in choices:
                print(f"ID: {choice['menu_id']}, Name: {choice['name']}")

            menu_id = int(input("Enter menu ID to give feedback: "))
            if menu_id not in [choice['menu_id'] for choice in choices]:
                print("Invalid menu ID. Please choose a valid menu item.")
                return True

            comment = input("Enter comment: ")
            rating = int(input("Enter rating (1-5): "))
            feedback = Feedback(employee_id, menu_id, comment, rating)
            feedback.add()

            query = "UPDATE choices SET feedback_given = 1 WHERE employee_id = %s AND menu_id = %s"
            cursor.execute(query, (employee_id, menu_id))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    elif choice == MENU_CHOICES['EMPLOYEE']['VIEW_FEEDBACK']:
        Feedback.view()
    elif choice == MENU_CHOICES['EMPLOYEE']['CHOOSE_RECOMMENDED_ITEM']:
        if Recommendation.has_already_chosen(employee_id):
            print("You have already chosen a menu item for today.")
            return True
        
        recommended_items = Recommendation.fetch_recommended_items()
        if recommended_items:
            print("Recommended Items for Next Day:")
            unique_items = {item[0]: item[1] for item in recommended_items}
            for item_id, name in unique_items.items():
                print(f"ID: {item_id}, Name: {name}")
            menu_id = int(input("Enter recommended menu ID to choose: "))
            Recommendation.choose_recommended_item(employee_id, menu_id)
        else:
            print("No recommended items available.")
    elif choice == MENU_CHOICES['EMPLOYEE']['VIEW_NOTIFICATIONS']:
        notifications = Notification.fetch_and_clear_notifications(employee_id)
        if notifications:
            print("Notifications:")
            for notification in notifications:
                print(f"Message: {notification['message']}, Date: {notification['created_at']}")
        else:
            print("No new notifications.")
    elif choice == MENU_CHOICES['EMPLOYEE']['LOGOUT']:
        return False
    else:
        print("Invalid choice. Please try again.")
    return True

def admin_menu():
    while True:
        display_admin_menu()
        choice = input("Enter choice: ")
        if not handle_admin_choice(choice):
            break

def chef_menu():
    while True:
        display_chef_menu()
        choice = input("Enter choice: ")
        if not handle_chef_choice(choice):
            break

def employee_menu(employee_id):
    while True:
        display_employee_menu()
        choice = input("Enter choice: ")
        if not handle_employee_choice(employee_id, choice):
            break

def reset_daily_data():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("TRUNCATE TABLE choices")
        cursor.execute("TRUNCATE TABLE recommendations")
        cursor.execute("DELETE FROM notifications WHERE is_read = 1")
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def main_menu():
    global current_date
    current_date = datetime.date.today()

    while True:
        display_main_menu()
        choice = input("Enter choice: ")
        if choice == MENU_CHOICES['MAIN']['LOGIN']:
            employee_id = input("Enter employee ID: ")
            password = input("Enter password: ")
            role = User.authenticate(employee_id, password)
            if role:
                print(f"Authenticated as {role}")
                if role == 'admin':
                    admin_menu()
                elif role == 'chef':
                    chef_menu()
                elif role == 'employee':
                    employee_menu(employee_id)
            else:
                print("Authentication failed. Please try again.")
        elif choice == MENU_CHOICES['MAIN']['REGISTER']:
            employee_id = input("Enter employee ID: ")
            name = input("Enter name: ")
            password = input("Enter password: ")
            role = input("Enter role (admin, chef, employee): ")
            user = User(employee_id, name, password, role)
            user.register()
        elif choice == MENU_CHOICES['MAIN']['NEXT_DAY']:
            current_date += datetime.timedelta(days=1)
            reset_daily_data()
            print(f"Simulated date: {current_date}")
            print("Chef needs to log in and generate food recommendations for the next day.")
        elif choice == MENU_CHOICES['MAIN']['EXIT']:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
