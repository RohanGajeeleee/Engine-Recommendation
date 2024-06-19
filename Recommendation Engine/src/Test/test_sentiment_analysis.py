import unittest
import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.sentiment_analysis import analyze_sentiment, convert_score_to_sentiment

class TestSentimentAnalysis(unittest.TestCase):

    def test_analyze_sentiment_positive(self):
        comment = "This is an amazing product!"
        score = analyze_sentiment(comment)
        sentiment = convert_score_to_sentiment(score)
        self.assertEqual(sentiment, 'Positive')

    def test_analyze_sentiment_negative(self):
        comment = "This is a terrible product!"
        score = analyze_sentiment(comment)
        sentiment = convert_score_to_sentiment(score)
        self.assertEqual(sentiment, 'Negative')

    def test_analyze_sentiment_neutral(self):
        comment = "This product is okay."
        score = analyze_sentiment(comment)
        sentiment = convert_score_to_sentiment(score)
        self.assertEqual(sentiment, 'Neutral')

if __name__ == '__main__':
    unittest.main()
