import logging
from src.application.services.user_service import UserService
from src.application.services.menu_service import MenuService
from src.application.services.feedback_service import FeedbackService
from src.application.services.current_menu_service import CurrentMenuService
from src.application.services.recommendation_service import RecommendationService
from src.application.services.notification_service import NotificationService
from src.application.services.discard_service import DiscardService
from src.application.services.feedback_request_service import FeedbackRequestService
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
            elif command == "GENERATE_RECOMMENDATIONS":
                return RequestHandler.handle_generate_recommendations(parts)
            elif command == "FETCH_RECOMMENDATIONS":
                return RequestHandler.handle_fetch_recommendations(parts)
            elif command == "FINALIZE_CURRENT_MENU":
                return RequestHandler.handle_finalize_current_menu()
            elif command == "VIEW_DISCARDED_ITEMS":
                return RequestHandler.handle_view_discarded_items(parts)
            elif command == "VIEW_NOTIFICATIONS":
                return RequestHandler.handle_view_notifications(parts)
            elif command == "VIEW_DISCARDED_ITEMS":
                return RequestHandler.handle_view_discarded_items(parts)
            elif command == "RESTORE_DISCARDED_ITEM":
                return RequestHandler.handle_restore_discarded_item(parts)
            elif command == "DELETE_DISCARDED_ITEM":
                return RequestHandler.handle_delete_discarded_item(parts)
            elif command == "REQUEST_FEEDBACK_ON_DISCARDED_ITEM":
                return RequestHandler.handle_request_feedback_on_discarded_item(parts)
            elif command == "CHECK_DISCARDED_ITEMS":
                return RequestHandler.handle_check_discarded_items()
            elif command == "FETCH_FEEDBACK_REQUESTS":
                return RequestHandler.handle_fetch_feedback_requests(parts)
            elif command == "VIEW_FEEDBACK_REPLIES":
                return RequestHandler.handle_view_feedback_replies(parts)
            elif command == "REPLY_FEEDBACK_REQUEST":
                return RequestHandler.handle_reply_feedback_request(parts)
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
        NotificationService.send_to_all_employees(f"New menu item added: {name}")
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
        
        item_name = MenuService.get_item_name(item_id)
        
        response = MenuService.update_item(item_id, name, price, availability)
        NotificationService.send_to_all_employees(f"Menu item updated: {item_name if item_name else item_id}")
        return response

    @staticmethod
    def handle_delete_item(parts):
        if len(parts) != 2:
            return "Invalid DELETE_ITEM command format"
        _, item_id = parts
        item_id = int(item_id)
       
        item_name = MenuService.get_item_name(item_id)
        
        response = MenuService.delete_item(item_id)
        NotificationService.send_to_all_employees(f"Menu item deleted: {item_name if item_name else item_id}")
        return response

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
    @staticmethod
    def handle_generate_recommendations(parts):
        if len(parts) != 2:
            return "Invalid GENERATE_RECOMMENDATIONS command format"
        _, num_items = parts
        return RecommendationService.generate_custom_recommendations(int(num_items))
    @staticmethod
    def handle_fetch_recommendations(parts):
        if len(parts) != 2:
            return "Invalid FETCH_RECOMMENDATIONS command format"
        _, num_items = parts
        recommendations = RecommendationService.fetch_recommendations(int(num_items))
        response = "\nRecommendations:\n"
        for rec in recommendations:
            avg_rating = "No Rating" if rec['avg_rating'] is None or rec['avg_rating'] == 0 else f"{rec['avg_rating']:.2f}"
            response += f"ID: {rec['id']}, Name: {rec['name']}, Average Rating: {avg_rating}, Sentiment: {rec['sentiment']}\n"
        return response
    @staticmethod
    def handle_finalize_current_menu():
        new_menu_items = CurrentMenuService.finalize_current_menu()
        if isinstance(new_menu_items, str):  
            return new_menu_items
        NotificationService.send_new_menu_notification(new_menu_items)
        return "Menu finalized and notifications sent"
    @staticmethod
    def handle_view_notifications(parts):
        if len(parts) != 2:
            return "Invalid VIEW_NOTIFICATIONS command format"
        _, employee_id = parts
        return NotificationService.view_notifications(employee_id)
    @staticmethod
    def handle_view_discarded_items(parts):
        return DiscardService.view_discarded_items()

    @staticmethod
    def handle_restore_discarded_item(parts):
        if len(parts) != 2:
            return "Invalid RESTORE_DISCARDED_ITEM command format"
        _, item_id = parts
        return DiscardService.restore_item(item_id)

    @staticmethod
    def handle_delete_discarded_item(parts):
        if len(parts) != 2:
            return "Invalid DELETE_DISCARDED_ITEM command format"
        _, item_id = parts
        return DiscardService.delete_item(item_id)

    @staticmethod
    def handle_request_feedback_on_discarded_item(parts):
        if len(parts) != 2:
            return "Invalid REQUEST_FEEDBACK_ON_DISCARDED_ITEM command format"
        _, item_id = parts
        return DiscardService.request_feedback(item_id)
    @staticmethod
    def handle_fetch_feedback_requests(parts):
        if len(parts) != 2:
            return "Invalid FETCH_FEEDBACK_REQUESTS command format"
        _, employee_id = parts
        return FeedbackRequestService.fetch_feedback_requests(employee_id)

    @staticmethod
    def handle_reply_feedback_request(parts):
        if len(parts) < 7:
            return "Invalid REPLY_FEEDBACK_REQUEST command format"
        _, employee_id, request_id, menu_id, answer1, answer2, answer3 = parts
        return FeedbackRequestService.reply_feedback_request(employee_id, request_id, menu_id, answer1, answer2, answer3)
    @staticmethod
    def handle_check_discarded_items():
        DiscardService.move_to_discard_menu()
        return "Checked and moved items to discard menu"
    @staticmethod
    def handle_view_feedback_replies(parts):
        replies = FeedbackRequestService.fetch_feedback_replies()
        if not replies:
            return "No feedback replies available."
        
        response = "\nFeedback Replies:\n"
        for reply in replies:
            response += f"Notification ID: {reply['notification_id']}, Employee ID: {reply['employee_id']}, Reply: {reply['reply']}, Reply Date: {reply['reply_date']}\n"
        return response 