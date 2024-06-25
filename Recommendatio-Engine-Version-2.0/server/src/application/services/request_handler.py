import logging
from src.application.services.user_service import UserService
from src.application.services.menu_service import MenuService
from src.application.services.feedback_service import FeedbackService
from src.application.services.current_menu_service import CurrentMenuService

class RequestHandler:
    @staticmethod
    def handle_request(request):
        try:
            parts = request.split()
            command = parts[0]

            if command == "REGISTER":
                return RequestHandler.handle_register(parts)
            elif command == "AUTH":
                return RequestHandler.handle_auth(parts)
            elif command == "ADD_ITEM":
                return RequestHandler.handle_add_item(parts)
            elif command == "UPDATE_ITEM":
                return RequestHandler.handle_update_item(parts)
            elif command == "DELETE_ITEM":
                return RequestHandler.handle_delete_item(parts)
            elif command == "VIEW_MENU":
                return RequestHandler.handle_view_menu()
            elif command == "ADD_FEEDBACK":
                return RequestHandler.handle_add_feedback(parts)
            elif command == "VIEW_FEEDBACK":
                return FeedbackService.view_feedback()
            elif command == "VIEW_CURRENT_MENU":
                return CurrentMenuService.list_current_menu_items()
            elif command == "CHOOSE_RECOMMENDED_ITEM":
                return RequestHandler.handle_choose_recommended_item(parts)
            elif command == "FETCH_USER_CHOICES":
                return RequestHandler.handle_fetch_user_choices(parts)
            elif command == "CLEAR_CURRENT_MENU":
                return CurrentMenuService.clear_current_menu()
            elif command == "ADD_TO_CURRENT_MENU":
                return RequestHandler.handle_add_to_current_menu(parts)
            else:
                logging.warning(f"Invalid command: {command}")
                return "INVALID REQUEST"
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return f"Error handling request: {e}"

    @staticmethod
    def handle_register(parts):
        if len(parts) != 5:
            return "Invalid REGISTER command format"
        _, employee_id, name, password, role = parts
        return UserService.register_user(employee_id, name, password, role)

    @staticmethod
    def handle_auth(parts):
        if len(parts) != 3:
            return "Invalid AUTH command format"
        _, employee_id, password = parts
        role = UserService.authenticate_user(employee_id, password)
        if role:
            return f"Authenticated as {role}"
        return "Authentication failed"

    @staticmethod
    def handle_add_item(parts):
        if len(parts) != 4:
            return "Invalid ADD_ITEM command format"
        _, name, price, availability = parts
        return MenuService.add_item(name, float(price), availability)

    @staticmethod
    def handle_update_item(parts):
        if len(parts) != 5:
            return "Invalid UPDATE_ITEM command format"
        _, item_id, name, price, availability = parts
        item_id = int(item_id)
        name = None if name == "null" else name
        price = None if price == "null" else float(price)
        availability = None if availability == "null" else availability
        return MenuService.update_item(item_id, name, price, availability)

    @staticmethod
    def handle_delete_item(parts):
        if len(parts) != 2:
            return "Invalid DELETE_ITEM command format"
        _, item_id = parts
        return MenuService.delete_item(int(item_id))

    @staticmethod
    def handle_view_menu():
        items = MenuService.list_items()
        if isinstance(items, list):
            response = "\nMenu Items:\n"
            for item in items:
                response += f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}\n"
            return response
        return items

    @staticmethod
    def handle_add_feedback(parts):
        if len(parts) < 7:
            return "Invalid ADD_FEEDBACK command format"
        _, employee_id, menu_id, rating, *comment_parts, time_of_day, current_date = parts
        comment = " ".join(comment_parts)
        logging.debug(f"Received feedback request: employee_id={employee_id}, menu_id={menu_id}, rating={rating}, comment={comment}, time_of_day={time_of_day}, current_date={current_date}")
        return FeedbackService.add_feedback(employee_id, int(menu_id), int(rating), comment, current_date, time_of_day)

    @staticmethod
    def handle_choose_recommended_item(parts):
        if len(parts) != 4:
            return "Invalid CHOOSE_RECOMMENDED_ITEM command format"
        _, employee_id, item_id, time_of_day = parts
        return CurrentMenuService.choose_recommended_item(employee_id, int(item_id), time_of_day)
    @staticmethod
    def handle_fetch_user_choices(parts):
        if len(parts) != 3:
            return "Invalid FETCH_USER_CHOICES command format"
        _, employee_id, time_of_day = parts
        choices = FeedbackService.get_user_choices(employee_id, time_of_day)
        response = ""
        if choices:
            for choice in choices:
                response += f"ID: {choice['menu_id']}, Name: {choice['name']}\n"
        else:
            response = "No choices available."
        return response
    @staticmethod
    def handle_add_to_current_menu(parts):
        if len(parts) != 2:
            return "Invalid ADD_TO_CURRENT_MENU command format"
        _, item_id = parts
        return CurrentMenuService.add_item_to_current_menu(int(item_id))