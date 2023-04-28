import tkinter.messagebox
from tkinter import *
import os
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from google.cloud import speech, language_v1
from textToSpeech import Computer_Response

# parameter values for specific numbers needed in the functions below.
fs = 44100  # Sample rate
seconds = 10  # Duration of recording CHANGE VALUE FOR LONGER VOICE RECORDINGS
mp3_path = "./mp3_files/"
txt_path = "./text_files/"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './keys/strange-sun-377020-89492c5c249f.json'
# ^ This is the key for the authentication of the google cloud.
cloud_speech = speech.SpeechClient()  # Starts speech client
entity_details = {}  # List that will hold the entities found in the audio file.


def record_window():
    """
    This function prompts the user with a window to type the name of the file they want to create.
    :return: None
    """

    def branch_record():
        """
        Nested function that is called when the user presses the record button and directs them
        to the record_sound function.
        :return: None
        """
        global seconds
        # All code below is used to set the global seconds variable to the value entered by the
        # user.
        try:
            seconds = int(entry_box1.get())
        except ValueError:
            tkinter.messagebox.showerror(message="Please enter a valid number.")
            window.destroy()
            record_window()
        if seconds > 10:
            tkinter.messagebox.showerror(message="Larger than 10 seconds.")
            window.destroy()
            record_window()
        record_sound(entry_box.get(), window)

    # All code below is used to create the window that prompts the user to enter the name of the
    # file they want to create.
    window = Toplevel()
    label = Label(window, text="Enter the name of your file (No type extension)", padx=15)
    label.grid(column=0, row=0)
    entry_box = Entry(window)
    entry_box.grid(column=1, row=0)
    label1 = Label(window, text="Enter how long you would like to record for (Max 10 seconds)")
    label1.grid(column=0, row=1)
    entry_box1 = Entry(window)
    entry_box1.grid(column=1, row=1)
    button_ok = Button(window, text="Record", command=branch_record)
    button_ok.grid(column=1, row=2)
    button_cancel = Button(window, text="Cancel", command=window.destroy)
    button_cancel.grid(column=0, row=2)
    window.mainloop()


def record_sound(file_name, other_window):
    """
    This function is used to record a voice memo and save it as an mp3 file.
    :param file_name: The list of all the filenames selected from the left panel
    :param other_window: The record_window window to be destroyed, once the recording is finished.
    :return:
    """

    def update():
        """
        Helper function to update the window to show that the recording has taken place and has
        finished.
        :return: None
        """
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait(ignore_errors=False)
        write('output.wav', fs, my_recording)  # Save as WAV file
        sound = AudioSegment.from_wav('output.wav')
        sound.export(file_name + '.mp3', format='mp3')
        other_window.destroy()

        # Recording sound finishes. Shows the user that the recording is done.
        label.config(text="done.")
        button_ok = Button(window, text="ok", command=window.destroy)
        button_ok.grid(column=0, row=1)
        os.remove("./output.wav")
        os.replace("./" + file_name + ".mp3", "./mp3_files/" + file_name + ".mp3")
        refresh_listbox()

    # All code below is used to show the user that the file is recording.
    window = Toplevel()
    label = Label(window, text="Recording in progress...")
    label.grid(column=0, row=0)
    window.after(1000, update)
    window.mainloop()


def speech_analysis(file_name):
    """
    This function is used to perform a speech analysis on the selected mp3 files using
    the Google Cloud Speech API
    :param file_name: The list of all the filenames selected from the left panel
    :return: None
    """

    def update():
        """
        Helper function to update the window to show that the speech analysis has taken place and
        has finished.
        :return: None
        """
        config_mp3 = speech.RecognitionConfig(  # Sets the speech recognition configuration
            sample_rate_hertz=fs,
            enable_automatic_punctuation=FALSE,
            language_code='en-US'
        )
        with open(file_name[0] + file_name[1], 'rb') as f:  # opens the mp3 file and reads it in
            byte_data_mp3 = f.read()  # as bytes
        audio_mp3 = speech.RecognitionAudio(content=byte_data_mp3)

        response = cloud_speech.recognize(  # Performs the speech recognition on the mp3 file
            config=config_mp3,
            audio=audio_mp3
        )
        final_transcript = []
        final_transcript_confidence = []
        for result in response.results:  # Formatting the output of the result from gcloud
            alternative = result.alternatives[0]
            final_transcript_confidence.append(alternative.confidence)
            final_transcript.append(alternative.transcript)

        # Speech analysis finishes. Shows the user that the analysis is done.
        label.config(text="done.")
        button_ok = Button(window, text="ok", command=window.destroy)
        button_ok.grid(column=0, row=1)
        with open("./text_files/" + file_name[0][12:] + '.txt', 'w') as w:
            w.write(final_transcript[0])
            w.close()
        refresh_listbox()

    # parses the filename to make sure it is able to used.
    if len(file_name) > 1:
        tkinter.messagebox.showerror(message="Too many files selected from left panel.")
        return
    elif len(file_name) == 0:
        tkinter.messagebox.showerror(message="No file selected from left panel.")
        return
    # All code below is used to show the user that the speech analysis is taking place.
    file_name = os.path.splitext("./mp3_files/" + file_name[0])
    window = Toplevel()
    label = Label(window, text="Transcribing in progress...")
    label.grid(column=0, row=0)
    window.after(1000, update)
    window.mainloop()


def sentiment_analysis(file_name):
    """
    This function is used to perform a sentiment analysis on the selected txt files using
    the Google Cloud Natural Language API
    :param file_name: The list of the filenames selected
    :return: None
    """

    def update():
        """
        Helper function to update the window to show that the sentiment analysis has taken place and
        has finished.
        :return: None
        """
        with open(file_name[0] + file_name[1], 'r') as f:  # reads in the string from the txt file.
            data_txt = f.read()
        data_txt = data_txt.encode("utf-8")  # encodes the data to be used by the API
        sentiment_client = language_v1.LanguageServiceClient()
        type_ = language_v1.types.Document.Type.PLAIN_TEXT
        language = "en"
        document = {"content": data_txt, "type_": type_, "language": language}
        encoding_type = language_v1.EncodingType.UTF8
        response = sentiment_client.analyze_entity_sentiment(  # Performs the sentiment analysis
            request={"document": document, "encoding_type": encoding_type}
        )
        # Sentiment analysis finishes. Shows the user that the analysis is done.
        show_entity_sentiment(response)
        window.destroy()

        # TODO: response variable is the sentiment analysis object, need to pass it into the
        #  textToSpeech and then play the response

    # parses the filename to make sure it is able to used.
    if len(file_name) > 1:
        tkinter.messagebox.showerror(message="Too many files selected from right panel.")
        return
    elif len(file_name) == 0:
        tkinter.messagebox.showerror(message="No file selected from right panel.")
        return
    file_name = os.path.splitext("./text_files/" + file_name[0])

    # All code below is used to show the user that the sentiment analysis is taking place.
    window = Toplevel()
    label = Label(window, text="Sentiment Analysis in progress...")
    label.grid(column=0, row=0)
    window.after(1000, update)


def show_entity_sentiment(response):
    global entity_details
    window = Toplevel()
    listbox = Listbox(window)
    listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    listbox.bind("<Double-1>", lambda event: output_entity(get_listbox_selected(listbox)))
    button_done = Button(window, text="done", command=window.destroy)
    button_done.grid(column=1, row=1)
    # Loop through entities returned from the API
    i = 0
    for entity in response.entities:
        listbox.insert(i, entity.name)
        key = entity.name
        value = "Representative name for the entity: {}\n".format(entity.name) + \
                "Entity type: {}\n".format(language_v1.Entity.Type(entity.type_).name) + \
                "Salience score: {}\n".format(entity.salience) + \
                "Entity sentiment score: {}\n".format(entity.sentiment.score) + \
                "Entity sentiment magnitude: {}\n".format(entity.sentiment.magnitude)
        entity_details = {**entity_details, key : value}
        i += 1


def output_entity(entity_name):
    global entity_details
    window = Toplevel()
    label = Label(window, text=entity_details[entity_name[0]])
    label.grid(column=0, row=0)
    button_ok = Button(window, text="ok", command=window.destroy)
    button_ok.grid(column=0, row=1)


def output_txt(file_name):
    """
    This function is used to output the text file from the selected txt file. This is the code
    for when the listbox is double clicked.
    :param file_name: A list of all the file_names selected
    :return: None
    """

    # parses the filename to make sure it is able to used.
    if len(file_name) > 1:
        tkinter.messagebox.showerror(message="Too many files selected from right panel.")
        return
    elif len(file_name) == 0:
        tkinter.messagebox.showerror(message="No file selected from right panel.")
        return
    with open("./text_files/" + file_name[0], 'r') as f:
        data_txt = f.read()

    # All code below is used to show the user the text file.
    window = Toplevel()
    label = Label(window, text=data_txt)
    label.grid(column=0, row=0)
    button_ok = Button(window, text="ok", command=window.destroy)
    button_ok.grid(column=0, row=1)


def get_listbox_selected(listbox_local):
    """
    This function is used to get all the selected functions from the mp3 listbox
    :param listbox_local: listbox object
    :return: returns all the selected entries in the listbox
    """
    selection = []
    for index in listbox_local.curselection():
        selection.append(listbox_local.get(index))
    return selection


def refresh_listbox():
    """
    This function is used to refresh the listbox to show the user the updated list of files
    :return: None
    """
    load_directories()
    listbox_mp3.delete('0', 'end')
    listbox_text.delete('0', 'end')
    for i in range(len(directories_mp3)):
        listbox_mp3.insert(i, directories_mp3[i])
    for i in range(len(directories_txt)):
        listbox_text.insert(i, directories_txt[i])


def load_directories():
    """
    Helper function to refresh the directories used by the listbox
    :return: None
    """
    global directories_mp3
    global directories_txt
    # Populating of the directory with possible mp3 files
    directories_mp3 = os.listdir(mp3_path)
    directories_txt = os.listdir(txt_path)


def delete_files(listbox_local):
    """
    This function is used to delete the selected files from the listbox
    :param listbox_local: listbox object that the files are being deleted from.
    :return: None
    """
    path_name = None
    if listbox_local == listbox_mp3:
        path_name = mp3_path
    else:
        path_name = txt_path
    for index in listbox_local.curselection():
        os.remove(path_name + listbox_local.get(index))
    refresh_listbox()


# MAIN WINDOW FUNCTIONALITY
directories_mp3 = os.listdir(mp3_path)
directories_txt = os.listdir(txt_path)

# create the main window
root = Tk()
root.title("Sentiment Analyzer")
root.geometry("1200x1000")

# specify the grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

# create a Listbox in the first column
listbox_mp3 = Listbox(root)
listbox_mp3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
listbox_mp3.bind('<Delete>', lambda event: delete_files(listbox_mp3))

# create four Buttons in the second column
options_frame = Frame(root)
options_frame.grid(column=1, row=1, rowspan=1, pady=50, sticky="n")
title = Label(options_frame, text="Sentiment Analyzer")
title.grid(row=0, column=1, pady=125, sticky="n")
button_record = Button(options_frame, text="New Record", command=record_window)
button_record.grid(row=1, column=1, pady=25, sticky="n")
button_transcribe = Button(options_frame, text="Transcribe", command=lambda: speech_analysis(
    get_listbox_selected(listbox_mp3)))
button_transcribe.grid(row=2, column=1, pady=25, sticky="n")
button_sentiment = Button(options_frame, text="Perform\n Sentiment\n Analysis", command=lambda:
sentiment_analysis(get_listbox_selected(listbox_text)))
button_sentiment.grid(row=3, column=1, pady=25, sticky="n")
button_exit = Button(options_frame, text="Exit", command=root.destroy)
button_exit.grid(row=4, column=1, pady=25, sticky="n")

# create a Text widget in the third column
listbox_text = Listbox(root)
refresh_listbox()
listbox_text.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
listbox_text.bind('<Double-1>', lambda event: output_txt(get_listbox_selected(listbox_text)))
listbox_text.bind('<Delete>', lambda event: delete_files(listbox_text))

# center the widgets in each column
listbox_mp3.configure(width=20, height=5)
button_record.configure(width=10)
button_transcribe.configure(width=10)
button_sentiment.configure(width=10)
listbox_text.configure(width=30, height=5)

# start the event loop
root.mainloop()
