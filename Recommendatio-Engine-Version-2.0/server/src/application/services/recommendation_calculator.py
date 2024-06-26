from src.application.services.sentiment_analysis_service import SentimentAnalysisService
class RecommendationCalculator:
    @staticmethod
    def determine_recommendations(items, sentiments, threshold=3.0):
        sentiment_dict = {item['id']: 0 for item in items}
        for sentiment in sentiments:
            menu_id = sentiment[0]
            if menu_id not in sentiment_dict:
                sentiment_dict[menu_id] = 0
            sentiment_dict[menu_id] += sentiment[1]

        for item in items:
            item['sentiment_score'] = sentiment_dict.get(item['id'], 0)
            item['sentiment'] = SentimentAnalysisService.convert_score_to_sentiment(item['sentiment_score'])
            item['recommended'] = "Yes" if item['avg_rating'] is None or (item['avg_rating'] or 0) >= threshold else "No"

        return items
