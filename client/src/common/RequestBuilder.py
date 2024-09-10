class MenuRequestBuilder:
    @staticmethod
    def add_item_request(name, price, availability, spice_level, food_category, dietary_type):
        if ' ' in name:
            name = f'"{name}"'
        return f"ADD_ITEM {name} {price} {availability} {spice_level} {food_category} {dietary_type}"

    @staticmethod
    def update_item_request(item_id, name=None, price=None, availability=None, spice_level=None, food_category=None, dietary_type=None):
        return f"UPDATE_ITEM {item_id} {name if name else 'null'} {price if price else 'null'} {availability if availability else 'null'} {spice_level if spice_level else 'null'} {food_category if food_category else 'null'} {dietary_type if dietary_type else 'null'}"

    @staticmethod
    def delete_item_request(item_id):
        return f"DELETE_ITEM {item_id}"

    @staticmethod
    def fetch_sorted_menu_request(employee_id):
        return f"FETCH_SORTED_MENU {employee_id}"
    
    @staticmethod
    def view_menu_request():
        return "VIEW_MENU"
    
class FeedbackRequestBuilder:
    @staticmethod
    def add_feedback_request(employee_id, item_id, rating, comment, time_of_day, current_date):
        return f"ADD_FEEDBACK {employee_id} {item_id} {rating} {comment} {time_of_day} {current_date}"

    @staticmethod
    def fetch_feedback_requests_request(employee_id):
        return f"FETCH_FEEDBACK_REQUESTS {employee_id}"
    
    @staticmethod
    def view_feedback_request():
        return "VIEW_FEEDBACK"
    
    @staticmethod
    def request_feedback_on_discarded_item_request(item_id):
        return f"REQUEST_FEEDBACK_ON_DISCARDED_ITEM {item_id}"

    @staticmethod
    def view_feedback_replies_request():
        return "VIEW_FEEDBACK_REPLIES"
    
    @staticmethod
    def reply_feedback_request(employee_id, request_id, menu_id, q1, q2, q3):
        return f"REPLY_FEEDBACK_REQUEST {employee_id} {request_id} {menu_id} {q1} {q2} {q3}"
    
class CurrentMenuRequestBuilder:
    @staticmethod
    def clear_current_menu_request():
        return "CLEAR_CURRENT_MENU"
    
    @staticmethod
    def finalize_current_menu_request():
        return "FINALIZE_CURRENT_MENU"
    
    @staticmethod
    def add_to_current_menu_request(item_id):
        return f"ADD_TO_CURRENT_MENU {item_id}"
    
class DiscardMenuRequestBuilder:
    @staticmethod
    def check_discarded_items_request():
        return "CHECK_DISCARDED_ITEMS"
    @staticmethod
    def view_discarded_items_request():
        return "VIEW_DISCARDED_ITEMS"
    @staticmethod
    def restore_discarded_item_request(item_id):
        return f"RESTORE_DISCARDED_ITEM {item_id}"

    @staticmethod
    def delete_discarded_item_request(item_id):
        return f"DELETE_DISCARDED_ITEM {item_id}"
    
    
class RecommendationRequestBuilder:
    @staticmethod
    def generate_recommendations_request(num_recommendations):
        return f"GENERATE_RECOMMENDATIONS {num_recommendations}"

    @staticmethod
    def fetch_recommendations_request(num_recommendations):
        return f"FETCH_RECOMMENDATIONS {num_recommendations}"

    @staticmethod
    def choose_recommended_item_request(employee_id, item_id, time_of_day):
        return f"CHOOSE_RECOMMENDED_ITEM {employee_id} {item_id} {time_of_day}"
    
class NotificationRequestBuilder:
    @staticmethod
    def view_notifications_request(employee_id):
        return f"VIEW_NOTIFICATIONS {employee_id}"
    
class ProfileRequestBuilder:
    @staticmethod
    def update_profile_request(employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth):
        return f"UPDATE_PROFILE {employee_id} {dietary_preference} {spice_level} {cuisine_preference} {sweet_tooth}"

class UserRequestBuilder:
    @staticmethod
    def authenticate_request(employee_id, password):
        return f"AUTH {employee_id} {password}"
    
    @staticmethod
    def register_request(employee_id, name, password, role, profile_details):
        return f"REGISTER {employee_id} {name} {password} {role} {profile_details}"
