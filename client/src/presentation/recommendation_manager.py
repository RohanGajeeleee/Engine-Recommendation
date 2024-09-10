import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.input_validation import InputValidator
from src.common.RequestBuilder import MenuRequestBuilder
from src.common.RequestBuilder import RecommendationRequestBuilder
from src.common.menu_item_checker import MenuItemChecker

class RecommendationManager:
    def __init__(self):
        self.input_validator = InputValidator()
        self.menu_item_checker = MenuItemChecker()

    def generate_recommendations(self):
        try:
            num_recommendations = int(input("Enter the number of recommendations you want to generate: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return True

        request = RecommendationRequestBuilder.generate_recommendations_request(num_recommendations)
        response = send_request(request)
        print(response)

        fetch_request = RecommendationRequestBuilder.fetch_recommendations_request(num_recommendations)
        fetch_response = send_request(fetch_request)
        print(fetch_response)

        return True

    def choose_recommended_item(self, employee_id):
        request = MenuRequestBuilder.fetch_sorted_menu_request(employee_id)
        response = send_request(request)
        
        if response.startswith("No preferences found") or response.startswith("Error"):
            print(response)
            return False
        
        print(response)

        item_id = self.menu_item_checker.get_existing_current_item_id("Enter item ID to choose: ")
        time_of_day = self.input_validator.get_valid_time_of_day("Enter time of day (breakfast, lunch, dinner): ")
        request = RecommendationRequestBuilder.choose_recommended_item_request(employee_id, item_id, time_of_day)
        response = send_request(request)
        print(response)
        return True
