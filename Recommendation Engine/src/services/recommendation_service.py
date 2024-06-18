from src.models.recommendations import Recommendation

class RecommendationService:
    @staticmethod
    def list_all_menu_items():
        items = Recommendation.fetch_all_menu_items_with_details()
        if items:
            print("\nComplete Menu:")
            for item in items:
                avg_rating = item['avg_rating'] if item['avg_rating'] is not None else 0
                feedback_count = item['feedback_count'] if item['feedback_count'] is not None else 0
                sentiment = item['sentiment']
                recommended = item['recommended']
                print(f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}, Average Rating: {avg_rating:.2f}, Feedback Count: {feedback_count}, Sentiment: {sentiment}, Recommended: {recommended}")
        else:
            print("No menu items available.")

    @staticmethod
    def generate_recommendations():
        recommendations = Recommendation.recommend_items_for_next_day()
        RecommendationService.list_all_menu_items()
        return recommendations
    
    @staticmethod
    def choose_items_for_next_day():
        Recommendation.choose_items_for_next_day()
        return True

    @staticmethod
    def choose_recommended_item(employee_id):
        if Recommendation.has_already_chosen(employee_id):
            print("You have already chosen a menu item for today.")
            return True
        
        recommended_items = Recommendation.fetch_recommended_items_from_current_menu()
        if recommended_items:
            print("Recommended Items for Next Day:")
            for item in recommended_items:
                print(f"ID: {item[0]}, Name: {item[1]}")
            menu_id = int(input("Enter recommended menu ID to choose: "))
            if menu_id not in [item[0] for item in recommended_items]:
                print("Invalid menu ID. Please choose a valid recommended item.")
                return True
            Recommendation.choose_recommended_item(employee_id, menu_id)
        else:
            print("No recommended items available.")
        return True

    @staticmethod
    def confirm_menu_for_next_day():
        RecommendationService.generate_recommendations()
        chosen_items = []
        while True:
            menu_id = input("Enter menu ID to confirm (or 'done' to finish): ")
            if menu_id.lower() == 'done':
                if not chosen_items:
                    print("You must select at least one item.")
                    continue
                break
            try:
                menu_id = int(menu_id)
                chosen_items.append(menu_id)
            except ValueError:
                print("Invalid input. Please enter a valid integer menu ID.")
        
        Recommendation.confirm_menu_for_next_day(chosen_items)
        print("Menu for the next day has been confirmed.")
        return True
