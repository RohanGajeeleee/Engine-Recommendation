import os

class SentimentAnalysisService:
    @staticmethod
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

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    positive_words_path = os.path.join(base_path, 'positive_words.txt')
    negative_words_path = os.path.join(base_path, 'negative_words.txt')
    negations_path = os.path.join(base_path, 'negations.txt')

    positive_words = load_words_from_file(positive_words_path, is_weighted=True)
    negative_words = load_words_from_file(negative_words_path, is_weighted=True)
    negations = load_words_from_file(negations_path)

    @staticmethod
    def analyze_sentiment(comment):
        words = comment.lower().split()
        positive_score = 0
        negative_score = 0
        negation = False

        for word in words:
            if word in SentimentAnalysisService.negations:
                negation = not negation
            elif word in SentimentAnalysisService.positive_words:
                if negation:
                    negative_score += SentimentAnalysisService.positive_words[word]
                    negation = False
                else:
                    positive_score += SentimentAnalysisService.positive_words[word]
            elif word in SentimentAnalysisService.negative_words:
                if negation:
                    positive_score += SentimentAnalysisService.negative_words[word]
                    negation = False
                else:
                    negative_score += SentimentAnalysisService.negative_words[word]

        return positive_score - negative_score

    @staticmethod
    def convert_score_to_sentiment(score):
        if score > 0:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        else:
            return 'Neutral'
