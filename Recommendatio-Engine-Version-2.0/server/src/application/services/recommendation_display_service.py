# server/src/application/services/recommendation_display_service.py

class RecommendationDisplayService:
    @staticmethod
    def display_recommendations(items):
        print("Custom Recommendations:")
        for item in items:
            avg_rating = "No Rating" if item['avg_rating'] is None or item['avg_rating'] == 0 else f"{item['avg_rating']:.2f}"
            feedback_count = item['feedback_count'] if item['feedback_count'] is not None else 0
            sentiment = item['sentiment']
            recommended = item['recommended']
            print(f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']},  Average Rating: {avg_rating}, Feedback Count: {feedback_count}, Sentiment: {sentiment}, Recommended: {recommended}")
