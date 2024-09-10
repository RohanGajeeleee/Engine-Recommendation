import mysql.connector
from src.infrastructure.db_config import get_db_connection
from src.application.services.sentiment_analysis_service import SentimentAnalysisService

class SentimentRepository:
    def __init__(self):
        self.sentiment_analysis_service = SentimentAnalysisService()

    def fetch_sentiments(self):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT menu_id, comment FROM feedback"
            cursor.execute(query)
            results = cursor.fetchall()
            sentiments = [(menu_id, self.sentiment_analysis_service.analyze_sentiment(comment)) for menu_id, comment in results]
            return sentiments
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
