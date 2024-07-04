import os

class SentimentAnalysisService:
    def __init__(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
        self.positive_words_path = os.path.join(self.base_path, 'positive_words.txt')
        self.negative_words_path = os.path.join(self.base_path, 'negative_words.txt')
        self.negations_path = os.path.join(self.base_path, 'negations.txt')

        self.positive_words = self.load_words_from_file(self.positive_words_path, is_weighted=True)
        self.negative_words = self.load_words_from_file(self.negative_words_path, is_weighted=True)
        self.negations = self.load_words_from_file(self.negations_path)

    def load_words_from_file(self, file_path, is_weighted=False):
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

    def analyze_sentiment(self, comment):
        words = comment.lower().split()
        positive_score = 0
        negative_score = 0
        negation = False

        for word in words:
            if word in self.negations:
                negation = not negation
            elif word in self.positive_words:
                if negation:
                    negative_score += self.positive_words[word]
                    negation = False
                else:
                    positive_score += self.positive_words[word]
            elif word in self.negative_words:
                if negation:
                    positive_score += self.negative_words[word]
                    negation = False
                else:
                    negative_score += self.negative_words[word]

        return positive_score - negative_score

    def convert_score_to_sentiment(self, score):
        if score > 0:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        else:
            return 'Neutral'
