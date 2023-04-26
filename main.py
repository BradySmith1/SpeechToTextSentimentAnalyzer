import sys
from tkinter import *
import os
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import time


def record_window():
    window = Toplevel()
    label = Label(window, text="Enter the name of your file", padx=15)
    label.grid(column=0, row=0)
    entry_box = Entry(window)
    entry_box.grid(column=1, row=0)
    button_ok = Button(window, text="Record", command=lambda: [window.destroy(), record_sound(entry_box.get())])
    button_ok.grid(column=1, row=1)
    button_cancel = Button(window, text="Cancel", command=window.destroy)
    button_cancel.grid(column=0, row=1)


def record_sound(file_name):
    def update():
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, my_recording)  # Save as WAV file
        sound = AudioSegment.from_wav('output.wav')
        sound.export(file_name + '.mp3', format='mp3')

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


# parameter values for specific numbers needed in the functions below.
fs = 44100  # Sample rate
seconds = 3  # Duration of recording
start_path = "./mp3_files"

# Populating of the directory with possible mp3 files
directories = os.listdir(start_path)

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
for i in range(len(directories)):
    listbox.insert(i, directories[i])
listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# create three Buttons in the second column
options_frame = Frame(root)
options_frame.grid(column=1, row=1, rowspan=1, pady=50, sticky="n")
title = Label(options_frame, text="Sentiment Analyzer")
title.grid(row=0, column=1, pady=125, sticky="n")
button1 = Button(options_frame, text="New Record", command=record_window)
button1.grid(row=1, column=1, pady=25, sticky="n")
button2 = Button(options_frame, text="Transcribe")
button2.grid(row=2, column=1, pady=25, sticky="n")
button3 = Button(options_frame, text="Perform\n Sentiment\n Analysis")
button3.grid(row=3, column=1, pady=25, sticky="n")
button4 = Button(options_frame, text="Exit", command=root.destroy)
button4.grid(row=4, column=1, pady=25, sticky="n")

# create a Text widget in the third column
text = Text(root)
text.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# center the widgets in each column
listbox.configure(width=20, height=5)
button1.configure(width=10)
button2.configure(width=10)
button3.configure(width=10)
text.configure(width=30, height=5)

# start the event loop
root.mainloop()
