import logging
from src.infrastructure.repositories.discard_repository import DiscardRepository
from src.application.services.notification_service import NotificationService
from src.application.services.sentiment_analysis_service import SentimentAnalysisService

class DiscardService:
    def __init__(self):
        self.discard_repository = DiscardRepository()
        self.notification_service = NotificationService()
        self.sentiment_analysis_service = SentimentAnalysisService()

    def move_to_discard_menu(self):
        items_with_feedback = self.discard_repository.fetch_all_menu_items_with_feedback()
        item_feedback = self._aggregate_feedback(items_with_feedback)
        self._evaluate_and_discard_items(item_feedback)

    def _aggregate_feedback(self, items_with_feedback):
        item_feedback = {}
        for feedback in items_with_feedback:
            item_id = feedback['id']
            if item_id not in item_feedback:
                item_feedback[item_id] = {
                    'name': feedback['name'],
                    'price': feedback['price'],
                    'availability': feedback['availability'],
                    'spice_level': feedback['spice_level'],
                    'food_category': feedback['food_category'],
                    'dietary_type': feedback['dietary_type'],
                    'comments': [],
                    'ratings': []
                }
            item_feedback[item_id]['comments'].append(feedback['comment'])
            item_feedback[item_id]['ratings'].append(feedback['rating'])
        return item_feedback

    def _evaluate_and_discard_items(self, item_feedback):
        for item_id, data in item_feedback.items():
            avg_rating = sum(data['ratings']) / len(data['ratings']) if data['ratings'] else 0
            sentiment_score = sum(self.sentiment_analysis_service.analyze_sentiment(comment) for comment in data['comments'] if comment is not None)
            sentiment = self.sentiment_analysis_service.convert_score_to_sentiment(sentiment_score)
            if avg_rating < 2 and sentiment == 'Negative':
                self.discard_repository.move_item_to_discard({
                    'id': item_id,
                    'name': data['name'],
                    'price': data['price'],
                    'availability': data['availability'],
                    'spice_level': data['spice_level'],
                    'food_category': data['food_category'],
                    'dietary_type': data['dietary_type']
                }, avg_rating, sentiment)

    def view_discarded_items(self):
        try:
            discarded_items = self.discard_repository.get_discarded_items()
            if discarded_items:
                response = "\nDiscarded Items:\n"
                for item in discarded_items:
                    response += f"ID: {item['id']}, Name: {item['name']}\n"
                return response
            return "No discarded items available."
        except Exception as e:
            logging.error(f"Error viewing discarded items: {e}")
            return f"Error viewing discarded items: {e}"

    def restore_item(self, item_id):
        if not self.discard_repository.item_exists_in_discard(item_id):
            return "Error: Item does not exist in discarded items."
        try:
            self.discard_repository.restore_item(item_id)
            logging.info(f"Restored item ID: {item_id}")
            return "Item restored to menu successfully"
        except Exception as e:
            logging.error(f"Error restoring item: {e}")
            return f"Error restoring item: {e}"

    def delete_item(self, item_id):
        if not self.discard_repository.item_exists_in_discard(item_id):
            return "Error: Item does not exist in discarded items."
        try:
            self.discard_repository.delete_item(item_id)
            logging.info(f"Deleted item ID: {item_id} permanently")
            return "Item deleted permanently"
        except Exception as e:
            logging.error(f"Error deleting item: {e}")
            return f"Error deleting item: {e}"

    def request_feedback(self, item_id):
        try:
            item_name = self.discard_repository.get_item_name(item_id)
            if not item_name:
                return "Invalid item ID."
            message = (
                f"We are trying to improve your experience with {item_name} (MenuID: {item_id}). Please provide your feedback and help us.\n"
                f"Q1. What didn’t you like about {item_name}?\n"
                f"Q2. How would you like {item_name} to taste?\n"
                f"Q3. Share your mom’s recipe for {item_name}."
            )
            self.notification_service.send_to_all_employees(message)
            logging.info(f"Requested feedback for item ID: {item_id}")
            return "Feedback request sent successfully"
        except Exception as e:
            logging.error(f"Error requesting feedback: {e}")
            return f"Error requesting feedback: {e}"
