# server/src/application/services/user_service.py

import logging
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.menu_item_repository import MenuItemRepository
from src.domain.models.user import User
from src.domain.models.menu_item import MenuItem

logging.basicConfig(level=logging.INFO)

class UserService:
    @staticmethod
    def register_user(employee_id, name, password, role):
        try:
            user = User(employee_id=employee_id, name=name, password=password, role=role)
            UserRepository.save(user)
            logging.info(f"Registered user: {employee_id}")
            return "User registered successfully"
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return f"Error registering user: {e}"

    @staticmethod
    def authenticate_user(employee_id, password):
        try:
            user = UserRepository.find_by_id(employee_id)
            if user and user.check_password(password):
                logging.info(f"Authenticated user: {employee_id}")
                return user.role
            else:
                logging.warning(f"Authentication failed for user: {employee_id}")
                return "Authentication failed"
        except Exception as e:
            logging.error(f"Error authenticating user: {e}")
            return f"Error authenticating user: {e}"

class MenuService:
    @staticmethod
    def add_item(name, price, availability):
        try:
            menu_item = MenuItem(name=name, price=price, availability=availability)
            MenuItemRepository.add(menu_item)
            logging.info(f"Added menu item: {name}")
            return "Menu item added successfully"
        except Exception as e:
            logging.error(f"Error adding item: {e}")
            return f"Error adding item: {e}"

    @staticmethod
    def update_item(item_id, name=None, price=None, availability=None):
        try:
            menu_item = MenuItem(item_id=item_id, name=name, price=price, availability=availability)
            MenuItemRepository.update(menu_item)
            logging.info(f"Updated menu item ID: {item_id}")
            return "Menu item updated successfully"
        except Exception as e:
            logging.error(f"Error updating item: {e}")
            return f"Error updating item: {e}"

    @staticmethod
    def delete_item(item_id):
        try:
            MenuItemRepository.delete(item_id)
            logging.info(f"Deleted menu item ID: {item_id}")
            return "Menu item deleted successfully"
        except Exception as e:
            logging.error(f"Error deleting item: {e}")
            return f"Error deleting item: {e}"

    @staticmethod
    def list_items():
        try:
            items = MenuItemRepository.get_all()
            logging.info("Listed menu items")
            if items:
                response = "\nMenu Items:\n"
                for item in items:
                    response += f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}\n"
                return response
            return "No menu items available"
        except Exception as e:
            logging.error(f"Error listing items: {e}")
            return f"Error listing items: {e}"

class RequestHandler:
    @staticmethod
    def handle_request(request):
        try:
            parts = request.split()
            command = parts[0]

            if command == "REGISTER":
                if len(parts) != 5:
                    return "Invalid REGISTER command format"
                _, employee_id, name, password, role = parts
                return UserService.register_user(employee_id, name, password, role)

            elif command == "AUTH":
                if len(parts) != 3:
                    return "Invalid AUTH command format"
                _, employee_id, password = parts
                return UserService.authenticate_user(employee_id, password)

            elif command == "ADD_ITEM":
                if len(parts) != 4:
                    return "Invalid ADD_ITEM command format"
                _, name, price, availability = parts
                return MenuService.add_item(name, float(price), availability)

            elif command == "UPDATE_ITEM":
                if len(parts) != 5:
                    return "Invalid UPDATE_ITEM command format"
                _, item_id, name, price, availability = parts
                item_id = int(item_id)
                name = None if name == "null" else name
                price = None if price == "null" else float(price)
                availability = None if availability == "null" else availability
                return MenuService.update_item(item_id, name, price, availability)

            elif command == "DELETE_ITEM":
                if len(parts) != 2:
                    return "Invalid DELETE_ITEM command format"
                _, item_id = parts
                return MenuService.delete_item(int(item_id))

            elif command == "VIEW_MENU":
                return MenuService.list_items()

            else:
                logging.warning(f"Invalid command: {command}")
                return "INVALID REQUEST"
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return f"Error handling request: {e}"
