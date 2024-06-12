# src/sentiment_analysis.py

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

if __name__ == "__main__":
    comment = "The pasta was great but the service was terrible"
    sentiment = analyze_sentiment(comment)
    print(f"Sentiment: {sentiment}")
