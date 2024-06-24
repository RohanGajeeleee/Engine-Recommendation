import logging

class RequestHandler:
    @staticmethod
    def handle_request(request):
        try:
            from src.application.services.user_service import UserService
            from src.application.services.menu_service import MenuService
            
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
                role = UserService.authenticate_user(employee_id, password)
                if role:
                    return f"Authenticated as {role}"
                return "Authentication failed"

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
                items = MenuService.list_items()
                if isinstance(items, list):
                    response = "\nMenu Items:\n"
                    for item in items:
                        response += f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}\n"
                    return response
                return items 

            else:
                logging.warning(f"Invalid command: {command}")
                return "INVALID REQUEST"
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return f"Error handling request: {e}"
