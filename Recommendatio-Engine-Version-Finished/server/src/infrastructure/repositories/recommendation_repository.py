from src.infrastructure.repositories.menu_repository import MenuRepository
from src.infrastructure.repositories.sentiment_repository import SentimentRepository
from src.application.services.sentiment_analysis_service import SentimentAnalysisService
from src.application.services.recommendation_calculator import RecommendationCalculator

class RecommendationRepository:
    def __init__(self):
        self.menu_repository = MenuRepository()
        self.sentiment_repository = SentimentRepository()
        self.sentiment_analysis_service = SentimentAnalysisService()
        self.recommendation_calculator = RecommendationCalculator()

    def fetch_all_menu_items_with_details(self, threshold=3.0):
        items = self.menu_repository.fetch_all_menu_items()
        sentiments = self.sentiment_repository.fetch_sentiments()
        detailed_items = self.recommendation_calculator.determine_recommendations(items, sentiments, threshold)
        return detailed_items

    def fetch_recommended_items(self):
        items = self.menu_repository.fetch_all_menu_items()
        sentiments = self.sentiment_repository.fetch_sentiments()
        for item in items:
            item['sentiment_score'] = 0
            for sentiment in sentiments:
                if sentiment[0] == item['id']:
                    item['sentiment_score'] += sentiment[1]
            item['sentiment'] = self.sentiment_analysis_service.convert_score_to_sentiment(item['sentiment_score'])
            item['recommended'] = "Yes" if item['avg_rating'] is None or item['avg_rating'] >= 3 else "No"

        recommended_items = [item for item in items if item['recommended'] == "Yes"]
        return recommended_items
