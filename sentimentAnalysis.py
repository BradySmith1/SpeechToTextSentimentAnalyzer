from google.cloud import language_v1
import os
from textToSpeech import Computer_Response
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/strange-sun.json"

class SentimentAnalyzer:
    """
    This class models a sentiment analyzer, which will read from a given
    text file to analyze. Once a score of the sentiment is produced, this
    class will feed it to the computer's response.
    """

    def __init__(self):
        """
        Constructor for a sentiment analyzer that intializes the client and score
        :return: None
        """
        self.client = language_v1.LanguageServiceClient()
        self.score = 0


    def analyze(self, text_file):
        """
        Method to open the provided file and analyze the sentiment of its contents
        :param text_file: the file to be analyzed
        :return: None
        """
        try:
            with open(text_file, 'r') as file:
                text = file.read().replace('\n', '')
        except:
            print("Could not open file")
            exit()

        # prepare content of the text file
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # detects the sentiment of the text
        sentiment = self.client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        # receive score from the sentiment
        self.score = sentiment.score

    def analyze_entity_sentiment(self, text_file):
        try:
            with open(text_file, 'r') as file:
                text = file.read().replace('\n', '')
        except:
            print("Could not open file")
            exit()

        text = text.encode("utf-8")
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = language_v1.EncodingType.UTF8

        # Detects the sentiment of the text
        response = self.client.analyze_entity_sentiment(
            request={"document": document, "encoding_type": encoding_type}
        )

        return response

    def say_in_response(self):
        """
        Method to pass the current sentiment score to the computer response class
        and generate a response based on the statement's sentiment.
        :return: None
        """
        response = Computer_Response(self.score)
        response.generate_response()


    def get_score(self):
        """
        Getter for the sentiment score
        :return: the sentiment score
        """
        return self.score
