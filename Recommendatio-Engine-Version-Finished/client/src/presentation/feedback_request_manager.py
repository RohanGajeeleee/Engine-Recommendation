import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.input_validation import InputValidator

class FeedbackRequestManager:
    def __init__(self):
        self.input_validator = InputValidator()

    def reply_to_request(self, employee_id):
        request = f"FETCH_FEEDBACK_REQUESTS {employee_id}"
        response = send_request(request)
        feedback_requests = response.split('\n')
        
        feedback_requests = [req for req in feedback_requests if "ID:" in req]
        
        if not feedback_requests or feedback_requests[0].strip() == "":
            print("No feedback requests available.")
            return True

        print("\nFeedback Requests:")
        for i, request in enumerate(feedback_requests, start=1):
            print(f"{i}. {request}")

        choice = self.input_validator.get_valid_number("Select the request you want to reply to (number): ")
        if choice < 1 or choice > len(feedback_requests):
            print("Invalid choice.")
            return True

        selected_request = feedback_requests[choice - 1]

        if "ID: " not in selected_request:
            print("Invalid request format.")
            return True

        try:
            request_id = int(selected_request.split("ID: ")[1].split(",")[0])
            menu_id = int(selected_request.split("MenuID: ")[1].split(")")[0])
        except (IndexError, ValueError) as e:
            print(f"Error parsing request ID or menu ID: {e}")
            return True

        q1 = self.input_validator.get_valid_input("What didn’t you like about this item? ")
        q2 = self.input_validator.get_valid_input("How would you like this item to taste? ")
        q3 = self.input_validator.get_valid_input("Share your mom’s recipe for this item. ")

        feedback_reply = f"REPLY_FEEDBACK_REQUEST {employee_id} {request_id} {menu_id} {q1} {q2} {q3}"
        response = send_request(feedback_reply)
        print(response)
        return True
