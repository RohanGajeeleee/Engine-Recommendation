from src.infrastructure.repositories.menu_repository import MenuRepository
from src.infrastructure.repositories.sentiment_repository import SentimentRepository
from src.application.services.sentiment_analysis_service import SentimentAnalysisService
from src.application.services.recommendation_calculator import RecommendationCalculator

class RecommendationRepository:
    @staticmethod
    def fetch_all_menu_items_with_details(threshold=3.0):
        items = MenuRepository.fetch_all_menu_items()
        sentiments = SentimentRepository.fetch_sentiments()
        detailed_items = RecommendationCalculator.determine_recommendations(items, sentiments, threshold)
        return detailed_items

    @staticmethod
    def fetch_recommended_items():
        items = MenuRepository.fetch_all_menu_items()
        sentiments = SentimentRepository.fetch_sentiments()
        for item in items:
            item['sentiment_score'] = 0
            for sentiment in sentiments:
                if sentiment[0] == item['id']:
                    item['sentiment_score'] += sentiment[1]
            item['sentiment'] = SentimentAnalysisService.convert_score_to_sentiment(item['sentiment_score'])
            item['recommended'] = "Yes" if item['avg_rating'] is None or item['avg_rating'] >= 3 else "No"

        recommended_items = [item for item in items if item['recommended'] == "Yes"]
        return recommended_items
