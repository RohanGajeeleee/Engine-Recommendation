# client/src/common/choice_fetcher.py

from common.network_utils import send_request

class ChoiceFetcher:
    @staticmethod
    def fetch_user_choices(employee_id, time_of_day):
        request = f"FETCH_USER_CHOICES {employee_id} {time_of_day}"
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
