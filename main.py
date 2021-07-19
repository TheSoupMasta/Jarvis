from pytube import YouTube
from tkinter import filedialog
# The ttk module contains the progress bar widget
from tkinter import ttk
from tkinter import *
from wolframalpha import *
import cmath
import time
# Regular Expresion class (don't worry too much about this)
import re
import threading
#
BG_COLOUR = "#e3e3e3"
DEFAULT_FONT = "Arial"
#
#
#
# class Application:
#     def __init__(self, root):
#         self.root = root
#         self.root.grid_rowconfigure(0, weight=2)
#         self.root.grid_columnconfigure(0, weight=1)
#         self.root.config(bg=BG_COLOUR)
#
#         self.results = Label(window, text="", font=(DEFAULT_FONT, 15))
#         self.results.grid(column=0, row=0)
#         self.results1 = Label(window, text="", font=(DEFAULT_FONT, 15))
#         self.results1.grid(column=0, row=1)
#
#         self.mainmessage = Label(window, text="Please use me to solve the quadratic equation!", font=(DEFAULT_FONT, 50))
#         self.mainmessage.grid(pady=(5, 1))
#
#         self.message = Label(window, text="Please enter the value for a in ax^2+bx+c", font=(DEFAULT_FONT, 10))
#         self.message.grid(pady=(6, 1))
#         self.equation = Entry(window, width=10)
#         self.equation.grid(pady=(7, 1))
#
#         self.message = Label(window, text="Please enter the value for b in ax^2+bx+c", font=(DEFAULT_FONT, 10))
#         self.message.grid(pady=(8, 1))
#         self.equation1 = Entry(window, width=10)
#         self.equation1.grid(pady=(9, 1))
#
#         self.message = Label(window, text="Please enter the value for c in ax^2+bx+c", font=(DEFAULT_FONT, 10))
#         self.message.grid(pady=(10, 1))
#         self.equation2 = Entry(window, width=10)
#         self.equation2.grid(pady=(11, 1))
#
#         self.proceedbutton = Button(window, text="Proceed", command=self.clicked)
#         self.proceedbutton.grid(pady=(12, 1))
#
#     def clicked(self):
#         a = int(self.equation.get())
#         b = int(self.equation1.get())
#         c = int(self.equation2.get())
#         d = (b**2) - (4*a*c)
#
#         self.result1 = (-b-cmath.sqrt(d))/(2*a)
#         self.result2 = (-b+cmath.sqrt(d))/(2*a)
#
#         self.results.configure(text=self.result1)
#         self.results1.configure(text=self.result2)
#
#
#
#
#
#
# if __name__ == "__main__":
#
#     # Create an instance of the window using the built in class
#     window = Tk()
#     window.title("QuadraticEquationSolver")
#     # Fit the window to the full screen
#     window.state("normal")
#
#     app = Application(window)
#
#     # The mainloop() function runs like an infinite loop until the program is closed
#     mainloop()


import pyaudio
import wolframalpha
import PySimpleGUI as sg
import pyttsx3
import speech_recognition as sr
client = wolframalpha.Client("no peeking")
engine = pyttsx3.init()


class Jarvis():
    def __init__(self, mic_obj, rec_obj):
        self.mic = mic_obj
        self.r = rec_obj
        self.search_engine()


    def search_engine(self):
        sg.theme('DarkPurple')
        layout = [[sg.Text('Enter a command'), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Use Voice Recognition')]]
        self.window = sg.Window('PyDa', layout)

        while True:
            event, values = self.window.read()
            if event in (None, 'Cancel'):
                break
            if event in (None, 'Use Voice Recognition'):
                self.voicerecognition()
                break
            try:
                wolfram_res = next(client.query(values[0]).results).text
                engine.say(wolfram_res)
                sg.PopupNonBlocking("Wolfram Result: " + wolfram_res)
            except:
                quit('Error')


            engine.runAndWait()

        self.window.close()

    def voicerecognition(self):
        sg.theme('DarkPurple')
        layout = [[sg.Button("Press and Speak"), sg.Button('Cancel')]]
        self.speechrecogwindow = sg.Window("Speech Recognition Assistant", layout)

        while True:
            event, values = self.speechrecogwindow.read()
            if event in (None, "Press and Speak"):
                self.speechrecogwindow.close()
                self.recog(self.r)
                break
            if event in (sg.WIN_CLOSED, 'Cancel'):
                self.speechrecogwindow.close()
                quit()


    def recog(self, rec_obj):
        while True:
            wolfram_res = None
            with self.mic as source:
                print("Speak")
                rec_obj.adjust_for_ambient_noise(source)
                audio = rec_obj.listen(source)
                try:
                    response = rec_obj.recognize_google(audio)
                except(sr.UnknownValueError):
                    quit("Could not recognize")
            try:
                wolfram_res = next(client.query(response).results).text
                engine.say(wolfram_res)
                engine.runAndWait()
                layout = [[sg.Text(wolfram_res)], [sg.Button('Ok')]]
                self.popup = sg.Window('Popup', layout)
                while True:
                    event, values = self.popup.read()
                    if event in (sg.WIN_CLOSED, 'Ok'):
                        self.popup.close()
                        break
                self.voicerecognition()
            except(StopIteration):
                print("Could not find answer")
                self.voicerecognition()

if __name__ == "__main__":
    jarvis = Jarvis(sr.Microphone(), sr.Recognizer())







