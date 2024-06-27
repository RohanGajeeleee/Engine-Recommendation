import logging
from src.infrastructure.repositories.discard_repository import DiscardRepository
from src.application.services.notification_service import NotificationService
from src.application.services.sentiment_analysis_service import SentimentAnalysisService

class DiscardService:
    @staticmethod
    def move_to_discard_menu():
        items_with_feedback = DiscardRepository.fetch_all_menu_items_with_feedback()
        item_feedback = {}

        for feedback in items_with_feedback:
            item_id = feedback['id']
            if item_id not in item_feedback:
                item_feedback[item_id] = {
                    'name': feedback['name'],
                    'price': feedback['price'],
                    'availability': feedback['availability'],
                    'comments': [],
                    'ratings': []
                }
            item_feedback[item_id]['comments'].append(feedback['comment'])
            item_feedback[item_id]['ratings'].append(feedback['rating'])

        # Process each item's feedback
        for item_id, data in item_feedback.items():
            avg_rating = sum(data['ratings']) / len(data['ratings']) if data['ratings'] else 0
            sentiment_score = sum(SentimentAnalysisService.analyze_sentiment(comment) for comment in data['comments'] if comment is not None)
            sentiment = SentimentAnalysisService.convert_score_to_sentiment(sentiment_score)

            if avg_rating < 2 and sentiment == 'Negative':
                DiscardRepository.move_item_to_discard({
                    'id': item_id,
                    'name': data['name'],
                    'price': data['price'],
                    'availability': data['availability']
                }, avg_rating, sentiment)
    @staticmethod
    def view_discarded_items():
        try:
            discarded_items = DiscardRepository.get_discarded_items()
            if discarded_items:
                response = "\nDiscarded Items:\n"
                for item in discarded_items:
                    response += f"ID: {item['id']}, Name: {item['name']}\n"
                return response
            return "No discarded items available."
        except Exception as e:
            logging.error(f"Error viewing discarded items: {e}")
            return f"Error viewing discarded items: {e}"

    @staticmethod
    def restore_item(item_id):
        if not DiscardRepository.item_exists_in_discard(item_id):
            return "Error: Item does not exist in discarded items."
        try:
            DiscardRepository.restore_item(item_id)
            logging.info(f"Restored item ID: {item_id}")
            return "Item restored to menu successfully"
        except Exception as e:
            logging.error(f"Error restoring item: {e}")
            return f"Error restoring item: {e}"

    @staticmethod
    def delete_item(item_id):
        if not DiscardRepository.item_exists_in_discard(item_id):
            return "Error: Item does not exist in discarded items."
        try:
            DiscardRepository.delete_item(item_id)
            logging.info(f"Deleted item ID: {item_id} permanently")
            return "Item deleted permanently"
        except Exception as e:
            logging.error(f"Error deleting item: {e}")
            return f"Error deleting item: {e}"

    @staticmethod
    def request_feedback(item_id):
        try:
            item_name = DiscardRepository.get_item_name(item_id)
            if not item_name:
                return "Invalid item ID."
            message = (
                f"We are trying to improve your experience with {item_name} (MenuID: {item_id}). Please provide your feedback and help us.\n"
                f"Q1. What didn’t you like about {item_name}?\n"
                f"Q2. How would you like {item_name} to taste?\n"
                f"Q3. Share your mom’s recipe for {item_name}."
            )
            NotificationService.send_to_all_employees(message)
            logging.info(f"Requested feedback for item ID: {item_id}")
            return "Feedback request sent successfully"
        except Exception as e:
            logging.error(f"Error requesting feedback: {e}")
            return f"Error requesting feedback: {e}"