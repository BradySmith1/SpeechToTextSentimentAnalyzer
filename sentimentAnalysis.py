from google.cloud import language_v1
import os
import textToSpeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="services.json"

class Sentiment_Analyzer:
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

    def get_score(self):
        return self.score

def main() :
    text = Sentiment_Analyzer()
    text.analyze("text_files\\text.txt")
    response = textToSpeech.Computer_Response(text.get_score())
    response.generate_response();

main()