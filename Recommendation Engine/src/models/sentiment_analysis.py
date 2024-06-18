def analyze_sentiment(comment):
    positive_words = ['good', 'great', 'excellent', 'amazing', 'nice']
    negative_words = ['bad', 'poor', 'terrible', 'awful', 'worst']

    positive_count = sum(1 for word in comment.split() if word.lower() in positive_words)
    negative_count = sum(1 for word in comment.split() if word.lower() in negative_words)

    if positive_count > negative_count:
        return 'Positive'
    elif negative_count > positive_count:
        return 'Negative'
    else:
        return 'Neutral'

class SentimentAnalyzer:
    @staticmethod
    def analyze_feedback_comments():
        from src.models.recommendations import Recommendation
        db = Recommendation.get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT menu_id, comment FROM feedback"
            cursor.execute(query)
            results = cursor.fetchall()
            sentiments = []
            for menu_id, comment in results:
                sentiment = analyze_sentiment(comment)
                sentiments.append((menu_id, comment, sentiment))
            return sentiments
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
