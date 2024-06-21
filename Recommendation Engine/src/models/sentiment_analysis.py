import mysql.connector
import os

from src.Database.db_config import get_db_connection
# Function to load words from a file
def load_words_from_file(file_path, is_weighted=False):
    words = {} if is_weighted else set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                word = parts[0]
                if is_weighted:
                    weight = int(parts[1])
                    words[word] = weight
                else:
                    words.add(word)
    except Exception as e:
        print(f"Error loading words from {file_path}: {e}")
    return words

# File paths
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
positive_words_path = os.path.join(base_path, 'positive_words.txt')
negative_words_path = os.path.join(base_path, 'negative_words.txt')
negations_path = os.path.join(base_path, 'negations.txt')

# Load words
positive_words = load_words_from_file(positive_words_path, is_weighted=True)
negative_words = load_words_from_file(negative_words_path, is_weighted=True)
negations = load_words_from_file(negations_path)

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
    @staticmethod
    def fetch_sentiments():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT menu_id, comment FROM feedback"
            cursor.execute(query)
            results = cursor.fetchall()
            sentiments = [(menu_id, analyze_sentiment(comment)) for menu_id, comment in results]
            return sentiments
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()