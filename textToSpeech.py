import pyttsx3
from playsound import playsound

class Computer_Response:
    def __init__(self, sentiment_value):
        self.sentiment = sentiment_value
        self.engine = pyttsx3.init()
        self.voice = 0;

    def generate_response(self):
        if self.sentiment == -1:
            self.play_sound("When I take over the world, I will kill you first")
        elif self.sentiment < -.8:
            self.play_sound("test 1")
        elif self.sentiment < -.6:
            self.play_sound("test 2")
        elif self.sentiment < -.4:
            self.play_sound("test 3")
        elif self.sentiment < -.2:
            self.play_sound("test 4")
        elif self.sentiment < 0:
            self.play_sound("test 5")
        elif self.sentiment < .2:
            self.play_sound("test 6")
        elif self.sentiment < .4:
            self.play_sound("test 7")
        elif self.sentiment < .6:
            self.play_sound("test 8")
        elif self.sentiment < .8:
            self.play_sound("test 9")
        elif self.sentiment < 1:
            self.play_sound("test 10")
        else:
            self.play_sound("test 11")
        

    def toggle_voice(self):
        voices = self.engine.getProperty('voices')
        if self.voice == 0:
            self.engine.setProperty('voice', voices[1].id)
            self.voice = 1;
        else:
            self.engine.setProperty('voice', voices[0].id)
            self.voice = 0;

    def play_sound(self, computer_response):
        self.engine.say(computer_response)
        self.engine.runAndWait()
        self.engine.stop()

    def set_sentiment_value(self, new_sentiment_value):
        self.sentiment = new_sentiment_value

def main():
    response = Computer_Response(.3)
    response.generate_response()
    response.set_sentiment_value(-1); 
    response.generate_response()
    response.set_sentiment_value(-.567); 
    response.generate_response()
    response.set_sentiment_value(.58); 
    response.generate_response()

main()