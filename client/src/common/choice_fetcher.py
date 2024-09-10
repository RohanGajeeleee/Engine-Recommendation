from common.network_utils import send_request
import logging

class ChoiceFetcher:
    def __init__(self):
        self.request_format = "FETCH_USER_CHOICES {} {}"

    def fetch_user_choices(self, employee_id, time_of_day):
        request = self.request_format.format(employee_id, time_of_day)
        
        try:
            response = send_request(request)
            items = response.split('\n')
            user_choices = []
            
            for item in items:
                if item.startswith("ID:"):
                    parts = item.split(', ')
                    item_id = int(parts[0].split(':')[1].strip())
                    item_name = parts[1].split(':')[1].strip()
                    user_choices.append({'menu_id': item_id, 'name': item_name})
            
            return user_choices
        
        except Exception as e:
            logging.error(f"Error fetching user choices: {e}")
            return []
