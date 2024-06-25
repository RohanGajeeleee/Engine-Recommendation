# server/src/application/services/feedback_service.py

import logging
from src.infrastructure.repositories.feedback_repository import FeedbackRepository
from src.infrastructure.repositories.Choice_Repository import ChoiceRepository

logging.basicConfig(level=logging.INFO)

class FeedbackService:
    @staticmethod
    def add_feedback(employee_id, menu_id, rating, comment, current_date, time_of_day):
        try:
            logging.debug(f"Attempting to add feedback for employee_id: {employee_id}, menu_id: {menu_id}, time_of_day: {time_of_day}")
            if not FeedbackRepository.can_give_feedback(employee_id, menu_id, time_of_day):
                logging.debug(f"Feedback already given for employee_id: {employee_id}, menu_id: {menu_id}, time_of_day: {time_of_day}")
                return "Feedback already given for this item at the specified time of day."
            
            # Add feedback
            FeedbackRepository.add_feedback(employee_id, menu_id, comment, rating, current_date)
            
            # Mark feedback given
            FeedbackRepository.mark_feedback_given(employee_id, menu_id, time_of_day)
            
            # Remove the item from choices
            FeedbackRepository.remove_choice(employee_id, menu_id, time_of_day)
            
            logging.info(f"Feedback added for employee ID {employee_id}, menu ID {menu_id}, time of day {time_of_day}")
            return "Feedback added successfully"
        except Exception as e:
            logging.error(f"Error adding feedback: {e}")
            return f"Error adding feedback: {e}"
    def view_feedback():
        try:
            feedback_list = FeedbackRepository.get_all_feedback()
            if not feedback_list:
                return "No feedback available."
            response = "\nFeedback:\n"
            for feedback in feedback_list:
                response += f"ID: {feedback['id']}, Employee ID: {feedback['employee_id']}, Menu ID: {feedback['menu_id']}, Rating: {feedback['rating']}, Comment: {feedback['comment']}, Date: {feedback['feedback_date']}\n"
            return response
        except Exception as e:
            logging.error(f"Error viewing feedback: {e}")
            return f"Error viewing feedback: {e}"
    @staticmethod
    def get_user_choices(employee_id, time_of_day):
        try:
            choices = ChoiceRepository.get_choices_by_employee_and_time(employee_id, time_of_day)
            return choices
        except Exception as e:
            logging.error(f"Error fetching user choices: {e}")
            return []
