from gtts import gTTS
import speech_recognition as sr
import pyttsx3
import os
import re
import webbrowser
import smtplib
import requests
import datetime
import wikipedia
import json
from time import strftime
from bs4 import BeautifulSoup as soup

# pyttsx3 initiation

engine = pyttsx3.init()
#voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
#print(voices[0].id)
#engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 0.9)
engine.setProperty('rate', 100)

# declaration
greetings = ['hey there', 'hello', 'hi', 'Hai', 'hey!', 'hey']
question = ['how are you', ]
getout = ['exit', 'close', 'goodbye', 'thank you']


# speak function initiation

def speak(audio: object) -> object:
    engine.say(audio)
    engine.runAndWait()


# Exit


def getOut():
    exit()


def weath():
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    city = "Hyderabad"
    url = api_address + city
    json_data = requests.get(url).json()
    format_add = json_data['weather'][0]['description']
    print(format_add)
    speak(format_add)


# welcome note


hour = int(datetime.datetime.now().hour)
if hour >= 0 and hour < 12:
    speak("Good Morning!")

elif hour >= 12 and hour < 18:
    speak("Good Afternoon!")

else:
    speak("Good Evening!")

speak('I am Clushi. your Personal assistant')

speak('I am ready for your command')


# user command input fuction


def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        # playsound('/home/pi/Downloads/Interface-alert-sound.mp3')
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        # print('You said: ' + command + '\n')

    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()

    return command


# user questions and answers


def assistant(command):
    "if statements for executing commands"

    print(command)

    if 'time' in command:
        import datetime
        now = datetime.datetime.now()
        speak('Current time is %d hours %d minutes' % (now.hour, now.minute))

    elif 'when is your birthday' in command:
        speak('it is my birthday today')
        speak('bless me')

    elif 'what can you do' in command:
        speak('here are the things that i can do for you')
        speak(
            'i can tell you time , weather , search on wikipedia and playing your favourite music wil be added in the future')

    elif 'who made you' in command:
        speak('cse4c made me')

    elif 'wikipedia' in command:
        speak('Searching' + command)
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif command in greetings:
        speak('My name is Clushi. your favourite personal assistant')
        speak('And you must be the human!')

    elif command in getout:
        speak('bye sir. have a great day')
        getOut()

    elif 'what is your purpose' in command:
        speak('faculty took the initiation to create me , i am thankful to him')

    elif 'who designed you' in command:
        speak('aarsh designed me')

    elif 'who built you' in command:
        speak('niharika built me')

    elif 'who is your teacher' in command:
        speak('reshma is my teacher')


    elif 'what is your workplace' in command:
        speak('saint martins engineering college cse department')


    elif 'weather' in command:
        weath()

    elif "what is the weather" in command:
        weath()

    elif command in question:
        speak("What would you like to have along with it. roti or rice")

    elif 'im feeling good' in command:
        speak('good to hear. how can i help you?')

    else:
        speak('I don\'t know what you mean!')


# loop to continue executing multiple commands
while True:
    assistant(myCommand())