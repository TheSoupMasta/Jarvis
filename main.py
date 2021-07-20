
import pyaudio
import wolframalpha
import PySimpleGUI as sg
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
client = wolframalpha.Client("no peeking")
engine = pyttsx3.init()


class Jarvis():
    def __init__(self, mic_obj, rec_obj):
        self.mic = mic_obj
        self.r = rec_obj
        self.r.energy_threshold = 300
        self.search_engine()


    def search_engine(self):
        sg.theme('DarkPurple')
        layout = [[sg.Text('Enter a command'), sg.InputText()], [sg.Button('WolfRamAlpha'), sg.Button('Google'), sg.Button('Use Voice Recognition'), sg.Button('Cancel')]]
        self.window = sg.Window('PyDa', layout)

        while True:
            event, values = self.window.read()
            if event in (None, 'Cancel'):
                break
            if event in (None, 'Use Voice Recognition'):
                self.voicerecognition()
                break
            if event in (None, 'Google'):
                try:
                    wb.get().open_new_tab('https://www.google.com/search?q=' + values[0][0::])
                except:
                    print('Error')
                    self.search_engine()
            if event in (None, 'Ok'):
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
            if response.split()[0] != 'Google':
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
            elif response.split()[0] == 'Google':
                wb.get().open_new_tab('https://www.google.com/search?q=' + response[7::])
                self.voicerecognition()

if __name__ == "__main__":
    jarvis = Jarvis(sr.Microphone(), sr.Recognizer())







