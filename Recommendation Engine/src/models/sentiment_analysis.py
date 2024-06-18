# src/models/sentiment_analysis.py

import mysql.connector
positive_words = {
    'good': 1, 'great': 2, 'excellent': 3, 'amazing': 3, 'nice': 1,
    'wonderful': 3, 'fantastic': 3, 'positive': 2, 'love': 3, 'awesome': 3,
    'best': 2, 'like': 1, 'superb': 3, 'beautiful': 3, 'happy': 2,
    'delightful': 3, 'pleasant': 2, 'satisfactory': 2, 'enjoy': 2,
    'perfect': 3, 'splendid': 3, 'marvelous': 3, 'outstanding': 3,
    'brilliant': 3, 'favorable': 2, 'incredible': 3, 'fabulous': 3,
    'impressive': 3, 'magnificent': 3, 'phenomenal': 3, 'remarkable': 3,
    'awesome': 3, 'terrific': 3, 'fantabulous': 3
}

negative_words = {
    'bad': 1, 'poor': 2, 'terrible': 3, 'awful': 3, 'worst': 3,
    'horrible': 3, 'negative': 2, 'hate': 3, 'dislike': 1, 'worse': 2,
    'atrocious': 3, 'dreadful': 3, 'abysmal': 3, 'unpleasant': 2,
    'disappointing': 2, 'unhappy': 2, 'sad': 2, 'miserable': 3, 'pathetic': 3,
    'lousy': 3, 'terrifying': 3, 'disastrous': 3, 'poorly': 2, 'crappy': 3,
    'depressing': 3, 'shoddy': 3, 'inferior': 2, 'subpar': 2, 'lackluster': 2
}

negations = {'not', 'no', 'never', 'none', 'nothing', 'nowhere', 'neither', 'hardly', 'scarcely', 'barely'}

def analyze_sentiment(comment):
    words = comment.lower().split()
    positive_score = 0
    negative_score = 0
    negation = False

    for word in words:
        if word in negations:
            negation = not negation
        elif word in positive_words:
            if negation:
                negative_score += positive_words[word]
                negation = False
            else:
                positive_score += positive_words[word]
        elif word in negative_words:
            if negation:
                positive_score += negative_words[word]
                negation = False
            else:
                negative_score += negative_words[word]

    return positive_score - negative_score

def convert_score_to_sentiment(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
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
                score = analyze_sentiment(comment)
                sentiments.append((menu_id, comment, score))
            return sentiments
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
