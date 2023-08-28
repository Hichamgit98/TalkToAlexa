import datetime
import os
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia

Listener = sr.Recognizer()
# Initialize the engine with the voice of 'Alex' (index 1 in the 'voices' list)
alexa = pyttsx3.init()
voices = alexa.getProperty('voices')
alexa.setProperty('voice', voices[0].id)


def talk(text):
    alexa.say(text)
    alexa.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening.....")
            voice = Listener.listen(source)
            command = Listener.recognize_google(voice)
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:
        talk("Sorry, I didn't understand that.")
        command = ""
    except sr.RequestError:
        talk("Sorry, there was an issue with the speech recognition service.")
        command = ""
    return command


def run_alexa():
    command = take_command().lower()
    print(command)
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is: ' + time)
    elif 'what is about' in command:
        research = command.replace('what is about', '').strip()
        info = wikipedia.summary(research, 3)
        print(info)
        talk(info)
    elif 'love' in command:
        talk('Sorry, love gives me a headache.')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi, and I want to be surrounded by '
             'python and all the new programming languages.')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'open' in command:
        folder_path = "C:/Users/hicham_garroum/Documents"
        os.startfile(folder_path)
        talk("Opening the Documents folder.")
    else:
        talk('Please say the command again.')


while True:
    run_alexa()

