import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.presentation.feedback_manager import FeedbackManager
from src.presentation.recommendation_manager import RecommendationManager
from src.presentation.discard_menu_manager import DiscardMenuManager
from src.presentation.choose_menu_manager import ChooseMenuManager

class ChefMenu:
    MENU_CHOICES = {
        'VIEW_FEEDBACK': '1',
        'CHOOSE_MENU_ITEMS': '2',
        'GENERATE_RECOMMENDATIONS': '3',
        'DISCARD_MENU': '4',
        'LOGOUT': '5'
    }

    def __init__(self):
        self.feedback_manager = FeedbackManager()
        self.recommendation_manager = RecommendationManager()
        self.discard_menu_manager = DiscardMenuManager()
        self.choose_menu_manager = ChooseMenuManager()

    def display(self):
        print("\nChef Menu")
        print("1. View Feedback")
        print("2. Choose Menu Items")
        print("3. Generate Recommendations")
        print("4. View Discarded Items")
        print("5. Logout")

    def handle_choice(self, chef_id, choice):
        actions = {
            ChefMenu.MENU_CHOICES['VIEW_FEEDBACK']: self.feedback_manager.view_feedback,
            ChefMenu.MENU_CHOICES['CHOOSE_MENU_ITEMS']: self.choose_menu_manager.choose_menu_items,
            ChefMenu.MENU_CHOICES['GENERATE_RECOMMENDATIONS']: self.recommendation_manager.generate_recommendations,
            ChefMenu.MENU_CHOICES['DISCARD_MENU']: self.discard_menu_manager.show_discard_menu,
            ChefMenu.MENU_CHOICES['LOGOUT']: self.logout
        }
        action = actions.get(choice, self.invalid_choice)
        return action()

    def logout(self):
        print("Logged out successfully")
        return False

    def invalid_choice(self):
        print("Invalid choice. Please try again.")
        return True
