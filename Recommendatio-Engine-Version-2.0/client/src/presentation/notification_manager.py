import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request

class NotificationManager:
    def view_notifications(self, employee_id):
        request = f"VIEW_NOTIFICATIONS {employee_id}"
        response = send_request(request)
        print(response)
        return True
