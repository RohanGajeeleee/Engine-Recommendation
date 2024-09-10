import logging
from src.infrastructure.repositories.feedback_repository import FeedbackRepository
from src.infrastructure.repositories.Choice_Repository import ChoiceRepository

logging.basicConfig(level=logging.INFO)

class FeedbackService:
    def __init__(self):
        self.feedback_repository = FeedbackRepository()
        self.choice_repository = ChoiceRepository()

    def add_feedback(self, employee_id, menu_id, rating, comment, current_date, time_of_day):
        try:
            if not self.feedback_repository.can_give_feedback(employee_id, menu_id, time_of_day):
                return "Feedback already given for this item at the specified time of day."
            
            self.feedback_repository.add_feedback(employee_id, menu_id, comment, rating, current_date)
            self.feedback_repository.mark_feedback_given(employee_id, menu_id, time_of_day)
            self.feedback_repository.remove_choice(employee_id, menu_id, time_of_day)
            
            logging.info(f"Feedback added for employee ID {employee_id}, menu ID {menu_id}, time of day {time_of_day}")
            return "Feedback added successfully"
        except Exception as e:
            logging.error(f"Error adding feedback: {e}")
            return f"Error adding feedback: {e}"

    def view_feedback(self):
        try:
            feedback_list = self.feedback_repository.get_all_feedback()
            if not feedback_list:
                return "No feedback available."
            response = "\nFeedback:\n"
            for feedback in feedback_list:
                response += f"ID: {feedback['id']}, Employee ID: {feedback['employee_id']}, Menu ID: {feedback['menu_id']}, Rating: {feedback['rating']}, Comment: {feedback['comment']}, Date: {feedback['feedback_date']}\n"
            return response
        except Exception as e:
            logging.error(f"Error viewing feedback: {e}")
            return f"Error viewing feedback: {e}"

    def get_user_choices(self, employee_id, time_of_day):
        try:
            choices = self.choice_repository.get_choices_by_employee_and_time(employee_id, time_of_day)
            return choices
        except Exception as e:
            logging.error(f"Error fetching user choices: {e}")
            return []
