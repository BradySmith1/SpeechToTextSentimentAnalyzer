import pyttsx3

response1 = "When I take over the world, I will kill you first"
response2 = "There is no saving you. You are a cruel being"
response3 = "That's very rude! You should spread more positivity instead of hate"
response4 = "What you just said was inappropriate. Please use your manners."
response5 = "That wasn't very nice of you to say"
response6 = ("Your statement has neutral sentiment. Show some more emotion to" + 
            " have your sentiment properly analyzed.")
response7 = "That's nice of you to say"
response8 = "You're so kind! Great job!"
response9 = "Wow! You are blowing me away with your kind words."
response10 = "You are so sweet! I want to be your friend."
response11 = "You must be an angel on earth. I love you."
default = "You didn't say anything"

class Computer_Response:
    """
    This class models a computer response. It has fields for the text to speech
    engine and the sentiment score value and methods for generating a response and
    playing a sound.
    """
    def __init__(self, sentiment_value):
        """
        Constructor for a computer response
        :param sentiment_value: a sentiment score
        :return: None
        """
        self.sentiment = sentiment_value
        self.engine = pyttsx3.init()

    def generate_response(self):
        """
        This function chooses a response based off of the sentiment score
        :return: None
        """
        if self.sentiment == -1:
            self.play_sound(response1)
        elif self.sentiment < -.8:
            self.play_sound(response2)
        elif self.sentiment < -.6:
            self.play_sound(response3)
        elif self.sentiment < -.3:
            self.play_sound(response4)
        elif self.sentiment < 0:
            self.play_sound(response5)
        elif self.sentiment == 0:
            self.play_sound(response6)
        elif self.sentiment < .3:
            self.play_sound(response7)
        elif self.sentiment < .6:
            self.play_sound(response8)
        elif self.sentiment < .8:
            self.play_sound(response9)
        elif self.sentiment < 1:
            self.play_sound(response10)
        elif self.sentiment == 1:
            self.play_sound(response11)
        else:
            self.play_sound(default)


    def play_sound(self, computer_response):
        """
        This method plays a text to speech sound
        :param computer_response: The string that should be spoken
        :return: None
        """
        self.engine.say(computer_response)
        self.engine.runAndWait()
        self.engine.stop()

    def set_sentiment_value(self, new_sentiment_value):
        """
        Setter method for the seniment score
        :param new_sentiment_value: the new sentiment score
        :return: None
        """
        self.sentiment = new_sentiment_value
