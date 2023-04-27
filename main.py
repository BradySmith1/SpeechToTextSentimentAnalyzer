import tkinter.messagebox
from tkinter import *
import os
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from google.cloud import speech
from textToSpeech import Computer_Response

# parameter values for specific numbers needed in the functions below.
fs = 44100  # Sample rate
seconds = 3  # Duration of recording
mp3_path = "./mp3_files"
txt_path = "./text_files"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './keys/strange-sun-377020-89492c5c249f.json'
cloud_speech = speech.SpeechClient()


def record_window():
    """
    This function prompts the user with a window to type the name of the file they want to create.
    :return: None
    """
    window = Toplevel()
    label = Label(window, text="Enter the name of your file", padx=15)
    label.grid(column=0, row=0)
    entry_box = Entry(window)
    entry_box.grid(column=1, row=0)
    button_ok = Button(window, text="Record", command=lambda: record_sound(entry_box.get(), window))
    button_ok.grid(column=1, row=1)
    button_cancel = Button(window, text="Cancel", command=window.destroy)
    button_cancel.grid(column=0, row=1)


def record_sound(file_name, other_window):
    """
    This function is used to record a voice memo and save it as an mp3 file.
    :param file_name: The list of all the filenames selected from the left panel
    :param other_window: The record_window window to be destroyed, once the recording is finished.
    :return:
    """

    def update():
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, my_recording)  # Save as WAV file
        sound = AudioSegment.from_wav('output.wav')
        sound.export(file_name + '.mp3', format='mp3')
        other_window.destroy()

        # Recording sound finishes.
        label.config(text="done.")
        button_ok = Button(window, text="ok", command=window.destroy)
        button_ok.grid(column=0, row=1)
        os.remove("./output.wav")
        os.replace("./" + file_name + ".mp3", "./mp3_files/" + file_name + ".mp3")

    window = Toplevel()
    label = Label(window, text="Recording in progress...")
    label.grid(column=0, row=0)
    window.after(1000, update)
    window.mainloop()


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


def speech_analysis(file_name):
    """
    This function is used to perform a speech analysis on the selected mp3 files using
    the Google Cloud Speech API
    :param file_name: The list of all the filenames selected from the left panel
    :return: None
    """

    def update():
        config_mp3 = speech.RecognitionConfig(
            sample_rate_hertz=fs,
            enable_automatic_punctuation=TRUE,
            language_code='en-US'
        )
        with open(file_name[0] + file_name[1], 'rb') as f:
            byte_data_mp3 = f.read()
        audio_mp3 = speech.RecognitionAudio(content=byte_data_mp3)

        response = cloud_speech.recognize(
            config=config_mp3,
            audio=audio_mp3
        )
        final_transcript = []
        final_transcript_confidence = []
        for result in response.results:
            alternative = result.alternatives[0]
            final_transcript_confidence.append(alternative.confidence)
            final_transcript.append(alternative.transcript)

        label.config(text="done.")
        button_ok = Button(window, text="ok", command=window.destroy)
        button_ok.grid(column=0, row=1)
        with open("./text_files/" + file_name[0][12:] + '.txt', 'w') as w:
            w.write(final_transcript[0])
            w.close()

    if len(file_name) > 1:
        tkinter.messagebox.showerror(message="Too many files selected from left panel.")
        return
    elif len(file_name) == 0:
        tkinter.messagebox.showerror(message="No file selected from left panel.")
        return
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
    from google.cloud import language_v1
    def update():
        with open(file_name[0] + file_name[1], 'r') as f:
            data_txt = f.read()
        data_txt = data_txt.encode("utf-8")
        sentiment_client = language_v1.LanguageServiceClient()
        type_ = language_v1.types.Document.Type.PLAIN_TEXT
        language = "en"
        document = {"content": data_txt, "type_": type_, "language": language}
        encoding_type = language_v1.EncodingType.UTF8
        response = sentiment_client.analyze_entity_sentiment(
            request={"document": document, "encoding_type": encoding_type}
        )
        label.config(text="done.")
        button_ok = Button(window, text="ok", command=window.destroy)
        button_ok.grid(column=0, row=1)
        # TODO: response variable is the sentiment analysis object, need to pass it into the
        #  textToSpeech and then play the response

    if len(file_name) > 1:
        tkinter.messagebox.showerror(message="Too many files selected from right panel.")
        return
    elif len(file_name) == 0:
        tkinter.messagebox.showerror(message="No file selected from right panel.")
        return
    file_name = os.path.splitext("./text_files/" + file_name[0])
    window = Toplevel()
    label = Label(window, text="Sentiment Analysis in progress...")
    label.grid(column=0, row=0)
    window.after(1000, update)


def output_txt(file_name):
    """
    This function is used to output the text file from the selected txt file
    :param file_name: A list of all the file_names selected
    :return: None
    """
    if len(file_name) > 1:
        tkinter.messagebox.showerror(message="Too many files selected from right panel.")
        return
    elif len(file_name) == 0:
        tkinter.messagebox.showerror(message="No file selected from right panel.")
        return
    with open("./text_files/" + file_name[0], 'r') as f:
        data_txt = f.read()
    window = Toplevel()
    label = Label(window, text=data_txt)
    label.grid(column=0, row=0)
    button_ok = Button(window, text="ok", command=window.destroy)
    button_ok.grid(column=0, row=1)


def main():
    """
    Main function for the GUI, sets up the main window
    :return: None
    """
    # Populating of the directory with possible mp3 files
    directories_mp3 = os.listdir(mp3_path)
    directories_txt = os.listdir(txt_path)

    # create the main window
    root = Tk()
    root.title("GUI with 3 Columns")
    root.geometry("1200x1000")

    # calculate the vertical center of the window
    window_height = root.winfo_reqheight()
    screen_height = root.winfo_screenheight()
    y = (screen_height - window_height) // 2

    # specify the grid layout
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(1, weight=1)

    # create a Listbox in the first column
    listbox = Listbox(root)
    for i in range(len(directories_mp3)):
        listbox.insert(i, directories_mp3[i])
    listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # create three Buttons in the second column
    options_frame = Frame(root)
    options_frame.grid(column=1, row=1, rowspan=1, pady=50, sticky="n")
    title = Label(options_frame, text="Sentiment Analyzer")
    title.grid(row=0, column=1, pady=125, sticky="n")
    button1 = Button(options_frame, text="New Record", command=record_window)
    button1.grid(row=1, column=1, pady=25, sticky="n")
    button2 = Button(options_frame, text="Transcribe", command=lambda: speech_analysis(
        get_listbox_selected(listbox)))
    button2.grid(row=2, column=1, pady=25, sticky="n")
    button3 = Button(options_frame, text="Perform\n Sentiment\n Analysis", command=lambda:
    sentiment_analysis(get_listbox_selected(text_listbox)))
    button3.grid(row=3, column=1, pady=25, sticky="n")
    button4 = Button(options_frame, text="Exit", command=root.destroy)
    button4.grid(row=4, column=1, pady=25, sticky="n")

    # create a Text widget in the third column
    text_listbox = Listbox(root)
    for n in range(len(directories_txt)):
        text_listbox.insert(n, directories_txt[n])
    text_listbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
    text_listbox.bind('<Double-1>', lambda event: output_txt(get_listbox_selected(text_listbox)))

    # center the widgets in each column
    listbox.configure(width=20, height=5)
    button1.configure(width=10)
    button2.configure(width=10)
    button3.configure(width=10)
    text_listbox.configure(width=30, height=5)

    # start the event loop
    root.mainloop()


if __name__ == "__main__":
    main()
