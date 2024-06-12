from src.models.recommendations import Recommendation

class RecommendationService:
    @staticmethod
    def generate_recommendations():
        recommendations = Recommendation.recommend_items_for_next_day()
        recommendation_data = Recommendation.get_recommendation_data(recommendations)
        print("Items recommended for next day.")
        for data in recommendation_data:
            avg_rating = data[1] if data[1] is not None else 0
            feedback_count = data[2] if data[2] is not None else 0
            print(f"Menu Item: {data[0]}, Average Rating: {avg_rating:.2f}, Feedback Count: {feedback_count}")
        sentiments = Recommendation.analyze_feedback_comments()
        for sentiment in sentiments:
            print(f"Menu ID: {sentiment[0]}, Comment: {sentiment[1]}, Sentiment: {sentiment[2]}")
        return True

    @staticmethod
    def choose_recommended_item(employee_id):
        if Recommendation.has_already_chosen(employee_id):
            print("You have already chosen a menu item for today.")
            return True
        
        recommended_items = Recommendation.fetch_recommended_items()
        if recommended_items:
            print("Recommended Items for Next Day:")
            unique_items = {item[0]: item[1] for item in recommended_items}
            for item_id, name in unique_items.items():
                print(f"ID: {item_id}, Name: {name}")
            menu_id = int(input("Enter recommended menu ID to choose: "))
            if menu_id not in unique_items.keys():
                print("Invalid menu ID. Please choose a valid recommended item.")
                return True
            Recommendation.choose_recommended_item(employee_id, menu_id)
        else:
            print("No recommended items available.")
        return True
