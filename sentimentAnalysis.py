from google.cloud import language_v1
import os
from textToSpeech import Computer_Response

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/strange-sun.json"


class SentimentAnalyzer:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        self.score = 0

    def analyze(self, text_file):
        try:
            with open(text_file, 'r') as file:
                text = file.read().replace('\n', '')
        except:
            print("Could not open file")
            exit()

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        sentiment = self.client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        self.score = sentiment.score

    def analyze_entity_sentiment(self, text_file):
        try:
            with open(text_file, 'r') as file:
                text = file.read().replace('\n', '')
        except:
            print("Could not open file")
            exit()

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        response = self.client.analyze_entity_sentiment(
            request={"document": document}
        )

        return response

    def say_in_response(self):
        response = Computer_Response(self.score)
        response.generate_response()

    def get_score(self):
        return self.score
