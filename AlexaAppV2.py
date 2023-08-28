import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x300+120+120")
root.iconbitmap('Google talk.ico')
root.resizable(False, False)

load = Image.open("df.png")
photo = ImageTk.PhotoImage(load)
label = tk.Label(root, image=photo)
label.image = photo
label.place(x=0, y=0)

Listener = sr.Recognizer()
alexa = pyttsx3.init()
voices = alexa.getProperty('voices')
alexa.setProperty('voice', voices[0].id)


# Function to send email
def send_email(subject, message, to_email):
    from_email = "your_email@gmail.com"
    app_password = "your_app_password"  # or your email account password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, app_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


# Function to get weather information
def get_weather_info():
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    api_key = 'd428ca471a580e3c08b4d64445b57b70'
    city = 'Delhi'

    url = base_url + 'appid=' + api_key + '&q=' + city

    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    city = response['name']
    sunrise = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    wind_speed = response['wind']['speed']
    description = response['weather'][0]['description']
    humidity = response['main']['humidity']

    weather_info = (
        f"Temperature in {city}: {temp_celsius:.2f} °C or {temp_fahrenheit:.2f}°F"
        f"Temperature in {city} feels like: {feels_like_celsius:.2f} °C or {feels_like_fahrenheit:.2f}°F"
        f"Humidity is: {humidity} %"
        f"Wind speed here: {wind_speed} km/h"
        f"General weather in {city}: {description}"
        f"The sun rises here at: {sunrise} Local time"
        f"The sun sets here at: {sunset} Local time"
    )

    talk(weather_info)
    # TODO Create an entry to set the city that we look for the weather
    # and connect it with this function as the city variable.


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


def start_listening():
    while True:
        run_alexa()


def send_email_command():
    subject = "Test Email"
    message = "This is a test email sent using the voice-controlled assistant."
    to_email = "recipient@example.com"
    send_email(subject, message, to_email)
    talk("Email sent successfully!")


"""def get_weather_command():
    city_name = "Casablanca"
    api_key = "your_openweathermap_api_key"
    weather_info = get_weather_info(city_name, api_key)
    talk(weather_info)"""

listen_button = tk.Button(root, text="Call Alexa",
                          font=('arial', 12, 'bold'),
                          fg='green', bg='black',
                          command=start_listening)
listen_button.place(x=285, y=40)

exit_button = tk.Button(root, text="Stop Alexa",
                        font=('arial', 12, 'bold'),
                        fg='green', bg='black',
                        command=root.quit)
exit_button.place(x=280, y=220)
email_button = tk.Button(root, text="Send Email",
                         font=('arial', 12, 'bold'),
                         fg='green', bg='black',
                         command=send_email_command)
email_button.place(x=280, y=100)

weather_button = tk.Button(root, text="Get Weather",
                           font=('arial', 12, 'bold'),
                           fg='green', bg='black',
                           command=get_weather_info)
weather_button.place(x=280, y=160)

root.mainloop()
