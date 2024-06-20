import mysql.connector
from src.Database.db_config import get_db_connection
from src.models.menu_management import MenuItem

class MenuService:
    @staticmethod
    def list_items():
        items = MenuItem.get_all_items()
        if items:
            print("\nMenu Items:")
            for item in items:
                print(f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}")
        else:
            print("No menu items available.")
        return True

    @staticmethod
    def add_item():
        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        
        while True:
            availability_choice = input("Enter availability (1 for Available, 2 for Unavailable): ")
            if availability_choice == '1':
                availability = 'Available'
                break
            elif availability_choice == '2':
                availability = 'Unavailable'
                break
            else:
                print("Invalid choice. Please enter 1 for Available or 2 for Unavailable.")
        
        menu_item = MenuItem(name=name, price=price, availability=availability)
        try:
            menu_item.add()
            print("Menu item added successfully")
        except Exception as e:
            print(f"Error adding menu item: {e}")
        return True

    @staticmethod
    def update_item():
        MenuService.list_items()
        item_id = int(input("Enter item ID to update: "))
        name = input("Enter new name (or leave blank to keep current): ")
        price = input("Enter new price (or leave blank to keep current): ")
        availability = None
        
        while True:
            availability_choice = input("Enter new availability (1 for Available, 2 for Unavailable, or leave blank to keep current): ")
            if availability_choice == '':
                break
            elif availability_choice == '1':
                availability = 'Available'
                break
            elif availability_choice == '2':
                availability = 'Unavailable'
                break
            else:
                print("Invalid choice. Please enter 1 for Available, 2 for Unavailable, or leave blank.")
        
        menu_item = MenuItem(item_id=item_id, name=name if name else None, price=float(price) if price else None, availability=availability)
        try:
            menu_item.update()
            print("Menu item updated successfully")
        except Exception as e:
            print(f"Error updating menu item: {e}")
        return True

    @staticmethod
    def delete_item():
        MenuService.list_items()
        item_id = int(input("Enter item ID to delete: "))
        menu_item = MenuItem(item_id=item_id)
        try:
            menu_item.delete()
            print("Menu item deleted successfully")
        except Exception as e:
            print(f"Error deleting menu item: {e}")
        return True
