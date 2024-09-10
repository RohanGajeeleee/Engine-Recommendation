import logging
from src.application.services.user_service import UserService
from src.application.services.menu_service import MenuService
from src.application.services.feedback_service import FeedbackService
from src.application.services.current_menu_service import CurrentMenuService
from src.application.services.recommendation_service import RecommendationService
from src.application.services.notification_service import NotificationService
from src.application.services.discard_service import DiscardService
from src.application.services.feedback_request_service import FeedbackRequestService
from src.application.services.profile_service import ProfileService

class RequestHandler:
    def __init__(self):
        self.user_service = UserService()
        self.menu_service = MenuService()
        self.feedback_service = FeedbackService()
        self.current_menu_service = CurrentMenuService()
        self.recommendation_service = RecommendationService()
        self.notification_service = NotificationService()
        self.discard_service = DiscardService()
        self.feedback_request_service = FeedbackRequestService()
        self.profile_service = ProfileService()

    def handle_request(self, request):
        try:
            parts = request.split()
            print(f"Request parts: {parts}")
            command = parts[0]

            if command == "REGISTER":
                return self.handle_register(parts)
            elif command == "AUTH":
                return self.handle_auth(parts)
            elif command == "ADD_ITEM":
                return self.handle_add_item(parts)
            elif command == "UPDATE_ITEM":
                return self.handle_update_item(parts)
            elif command == "DELETE_ITEM":
                return self.handle_delete_item(parts)
            elif command == "VIEW_MENU":
                return self.handle_view_menu()
            elif command == "ADD_FEEDBACK":
                return self.handle_add_feedback(parts)
            elif command == "VIEW_FEEDBACK":
                return self.feedback_service.view_feedback()
            elif command == "VIEW_CURRENT_MENU":
                return self.handle_view_current_menu()
            elif command == "CHOOSE_RECOMMENDED_ITEM":
                return self.handle_choose_recommended_item(parts)
            elif command == "FETCH_SORTED_MENU":
                return self.handle_fetch_sorted_menu(parts)
            elif command == "FETCH_USER_CHOICES":
                return self.handle_fetch_user_choices(parts)
            elif command == "CLEAR_CURRENT_MENU":
                return self.current_menu_service.clear_current_menu()
            elif command == "ADD_TO_CURRENT_MENU":
                return self.handle_add_to_current_menu(parts)
            elif command == "GENERATE_RECOMMENDATIONS":
                return self.handle_generate_recommendations(parts)
            elif command == "FETCH_RECOMMENDATIONS":
                return self.handle_fetch_recommendations(parts)
            elif command == "FINALIZE_CURRENT_MENU":
                return self.handle_finalize_current_menu()
            elif command == "VIEW_DISCARDED_ITEMS":
                return self.handle_view_discarded_items(parts)
            elif command == "VIEW_NOTIFICATIONS":
                return self.handle_view_notifications(parts)
            elif command == "VIEW_DISCARDED_ITEMS":
                return self.handle_view_discarded_items(parts)
            elif command == "RESTORE_DISCARDED_ITEM":
                return self.handle_restore_discarded_item(parts)
            elif command == "DELETE_DISCARDED_ITEM":
                return self.handle_delete_discarded_item(parts)
            elif command == "REQUEST_FEEDBACK_ON_DISCARDED_ITEM":
                return self.handle_request_feedback_on_discarded_item(parts)
            elif command == "CHECK_DISCARDED_ITEMS":
                return self.handle_check_discarded_items()
            elif command == "FETCH_FEEDBACK_REQUESTS":
                return self.handle_fetch_feedback_requests(parts)
            elif command == "VIEW_FEEDBACK_REPLIES":
                return self.handle_view_feedback_replies(parts)
            elif command == "REPLY_FEEDBACK_REQUEST":
                return self.handle_reply_feedback_request(parts)
            elif command == "UPDATE_PROFILE":
                return self.handle_update_profile(parts)
            else:
                logging.warning(f"Invalid command: {command}")
                return "INVALID REQUEST"
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return f"Error handling request: {e}"

    def handle_register(self, parts):
        if len(parts) < 5:
            return "Invalid REGISTER command format"
        
        _, employee_id, name, password, role = parts[:5]
        
        if role == 'employee' and len(parts) != 9:
            return "Invalid REGISTER command format for employee with profile"
        
        if role == 'employee':
            dietary_preference = parts[5]
            spice_level = parts[6]
            cuisine_preference = parts[7]
            sweet_tooth = parts[8]
            
            if sweet_tooth not in ['Yes', 'No']:
                return "Invalid value for sweet tooth"
        else:
            dietary_preference = spice_level = cuisine_preference = sweet_tooth = None

        response = self.user_service.register_user(employee_id, name, password, role, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
        
        return response

    def handle_auth(self, parts):
        if len(parts) != 3:
            return "Invalid AUTH command format"
        _, employee_id, password = parts
        role = self.user_service.authenticate_user(employee_id, password)
        if role:
            return f"Authenticated as {role}"
        return "Authentication failed"

    def handle_add_item(self, parts):
        full_request = ' '.join(parts)
        import shlex
        parts = shlex.split(full_request)

        if len(parts) < 7:
            return "Invalid ADD_ITEM command format"
        
        command = parts[0]
        name_parts = []
        i = 1
        while i < len(parts) and not parts[i].replace('.', '', 1).isdigit():
            name_parts.append(parts[i])
            i += 1
        
        name = " ".join(name_parts)
        
        if i >= len(parts) - 4:
            return "Invalid ADD_ITEM command format"

        price = parts[2]
        availability = parts[3]
        spice_level = parts[4]
        food_category = "-".join(parts[5:-1])
        dietary_type = parts[-1]
        
        return self.menu_service.add_item(name, float(price), availability, spice_level, food_category, dietary_type)

    def handle_update_item(self, parts):
        if len(parts) != 8:
            return "Invalid UPDATE_ITEM command format"
        
        _, item_id, name, price, availability, spice_level, food_category, dietary_type = parts
        item_id = int(item_id)
        name = None if name == "null" else name
        price = None if price == "null" else float(price)
        availability = None if availability == "null" else availability
        spice_level = None if spice_level == "null" else spice_level
        food_category = None if food_category == "null" else food_category
        dietary_type = None if dietary_type == "null" else dietary_type

        item_name = self.menu_service.get_item_name(item_id)
        
        response = self.menu_service.update_item(item_id, name, price, availability, spice_level, food_category, dietary_type)
        self.notification_service.send_to_all_employees(f"Menu item updated: {item_name if item_name else item_id}")
        return response


    def handle_delete_item(self, parts):
        if len(parts) != 2:
            return "Invalid DELETE_ITEM command format"
        _, item_id = parts
        item_id = int(item_id)
       
        item_name = self.menu_service.get_item_name(item_id)
        
        response = self.menu_service.delete_item(item_id)
        self.notification_service.send_to_all_employees(f"Menu item deleted: {item_name if item_name else item_id}")
        return response

    def handle_view_menu(self):
        items = self.menu_service.list_items()
        if isinstance(items, list):
            response = "\nMenu Items:\n"
            for item in items:
                response += f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}\n"
            return response
        return items

    def handle_add_feedback(self, parts):
        if len(parts) < 7:
            return "Invalid ADD_FEEDBACK command format"
        _, employee_id, menu_id, rating, *comment_parts, time_of_day, current_date = parts
        comment = " ".join(comment_parts)
        return self.feedback_service.add_feedback(employee_id, int(menu_id), int(rating), comment, current_date, time_of_day)

    def handle_choose_recommended_item(self, parts):
        if len(parts) != 4:
            return "Invalid CHOOSE_RECOMMENDED_ITEM command format"
        _, employee_id, item_id, time_of_day = parts
        response = self.current_menu_service.choose_recommended_item(employee_id, item_id, time_of_day)
        return response

    def handle_fetch_user_choices(self, parts):
        if len(parts) != 3:
            return "Invalid FETCH_USER_CHOICES command format"
        _, employee_id, time_of_day = parts
        choices = self.feedback_service.get_user_choices(employee_id, time_of_day)
        response = ""
        if choices:
            for choice in choices:
                response += f"ID: {choice['menu_id']}, Name: {choice['name']}\n"
        else:
            response = "No choices available."
        return response

    def handle_add_to_current_menu(self, parts):
        if len(parts) != 2:
            return "Invalid ADD_TO_CURRENT_MENU command format"
        _, item_id = parts
        return self.current_menu_service.add_item_to_current_menu(int(item_id))

    def handle_generate_recommendations(self, parts):
        if len(parts) != 2:
            return "Invalid GENERATE_RECOMMENDATIONS command format"
        _, num_items = parts
        return self.recommendation_service.generate_custom_recommendations(int(num_items))

    def handle_fetch_recommendations(self, parts):
        if len(parts) != 2:
            return "Invalid FETCH_RECOMMENDATIONS command format"
        _, num_items = parts
        recommendations = self.recommendation_service.fetch_recommendations(int(num_items))
        response = "\nRecommendations:\n"
        for rec in recommendations:
            avg_rating = "No Rating" if rec['avg_rating'] is None or rec['avg_rating'] == 0 else f"{rec['avg_rating']:.2f}"
            response += f"ID: {rec['id']}, Name: {rec['name']}, Average Rating: {avg_rating}, Sentiment: {rec['sentiment']}\n"
        return response

    def handle_finalize_current_menu(self):
        new_menu_items = self.current_menu_service.finalize_current_menu()
        if isinstance(new_menu_items, str):  
            return new_menu_items
        self.notification_service.send_new_menu_notification(new_menu_items)
        return "Menu finalized and notifications sent"

    def handle_view_notifications(self, parts):
        if len(parts) != 2:
            return "Invalid VIEW_NOTIFICATIONS command format"
        _, employee_id = parts
        return self.notification_service.view_notifications(employee_id)

    def handle_view_discarded_items(self, parts):
        return self.discard_service.view_discarded_items()

    def handle_restore_discarded_item(self, parts):
        if len(parts) != 2:
            return "Invalid RESTORE_DISCARDED_ITEM command format"
        _, item_id = parts
        return self.discard_service.restore_item(item_id)

    def handle_delete_discarded_item(self, parts):
        if len(parts) != 2:
            return "Invalid DELETE_DISCARDED_ITEM command format"
        _, item_id = parts
        return self.discard_service.delete_item(item_id)

    def handle_request_feedback_on_discarded_item(self, parts):
        if len(parts) != 2:
            return "Invalid REQUEST_FEEDBACK_ON_DISCARDED_ITEM command format"
        _, item_id = parts
        return self.discard_service.request_feedback(item_id)

    def handle_fetch_feedback_requests(self, parts):
        if len(parts) != 2:
            return "Invalid FETCH_FEEDBACK_REQUESTS command format"
        _, employee_id = parts
        return self.feedback_request_service.fetch_feedback_requests(employee_id)

    def handle_reply_feedback_request(self, parts):
        if len(parts) < 7:
            return "Invalid REPLY_FEEDBACK_REQUEST command format"
        _, employee_id, request_id, menu_id, answer1, answer2, answer3 = parts
        return self.feedback_request_service.reply_feedback_request(employee_id, request_id, menu_id, answer1, answer2, answer3)

    def handle_check_discarded_items(self):
        self.discard_service.move_to_discard_menu()
        return "Checked and moved items to discard menu"

    def handle_view_feedback_replies(self, parts):
        replies = self.feedback_request_service.fetch_feedback_replies()
        if not replies:
            return "No feedback replies available."
        
        response = "\nFeedback Replies:\n"
        for reply in replies:
            response += f"Notification ID: {reply['notification_id']}, Employee ID: {reply['employee_id']}, Reply: {reply['reply']}, Reply Date: {reply['reply_date']}\n"
        return response

    def handle_update_profile(self, parts):
        if len(parts) != 6:
            return "Invalid UPDATE_PROFILE command format"
        
        _, employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth = parts
        
        dietary_preference = None if dietary_preference == "null" else dietary_preference
        spice_level = None if spice_level == "null" else spice_level
        cuisine_preference = None if cuisine_preference == "null" else cuisine_preference
        sweet_tooth = None if sweet_tooth == "null" else sweet_tooth 
        
        response = self.profile_service.update_profile(employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
        return response

    def handle_fetch_sorted_menu(self, parts):
        if len(parts) != 2:
            return "Invalid FETCH_SORTED_MENU command format"
        
        _, employee_id = parts
        response = self.current_menu_service.get_sorted_menu_items_by_preferences(employee_id)
        return response

    def handle_view_current_menu(self):
        current_menu_items = self.current_menu_service.get_current_menu()
        if isinstance(current_menu_items, list):
            response = "\nCurrent Menu Items:\n"
            for item in current_menu_items:
                response += f"ID: {item['id']}, Name: {item['name']}\n"
            return response
        return current_menu_items
