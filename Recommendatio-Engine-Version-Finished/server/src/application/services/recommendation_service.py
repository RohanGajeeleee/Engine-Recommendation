import logging
from src.infrastructure.repositories.recommendation_repository import RecommendationRepository
from src.application.services.recommendation_display_service import RecommendationDisplayService

class RecommendationService:
    def __init__(self):
        self.recommendation_repository = RecommendationRepository()
        self.recommendation_display_service = RecommendationDisplayService()

    def generate_custom_recommendations(self, num_items):
        try:
            detailed_items = self.recommendation_repository.fetch_all_menu_items_with_details()
            recommended_items = self.filter_and_sort_recommendations(detailed_items)
            items_to_display = self.get_top_recommendations(recommended_items, num_items)
            
            self.recommendation_display_service.display_recommendations(items_to_display)
            return "Recommendations generated successfully"
        except Exception as e:
            logging.error(f"Error generating recommendations: {e}")
            return f"Error generating recommendations: {e}"

    def fetch_recommendations(self, num_items):
        try:
            recommended_items = self.recommendation_repository.fetch_recommended_items()
            recommended_items = self.filter_and_sort_recommendations(recommended_items)
            return self.get_top_recommendations(recommended_items, num_items)
        except Exception as e:
            logging.error(f"Error fetching recommendations: {e}")
            return []

    def filter_and_sort_recommendations(self, items):
        recommended_items = [item for item in items if item['recommended'] == "Yes"]
        recommended_items.sort(key=lambda x: x['avg_rating'] if x['avg_rating'] is not None else 0, reverse=True)
        return recommended_items

    def get_top_recommendations(self, recommended_items, num_items):
        if len(recommended_items) >= num_items:
            return recommended_items[:num_items]
        print(f"Only {len(recommended_items)} recommended items available to display.")
        return recommended_items
