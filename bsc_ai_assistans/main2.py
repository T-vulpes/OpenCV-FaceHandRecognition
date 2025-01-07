from datetime import datetime
import pyttsx3
import speech_recognition as sr
import csv
import re
import webbrowser

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  
    engine.say(command)
    engine.runAndWait()

def load_commands_from_csv(file_path):
    commands_dict = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            commands_dict[row['command']] = row['response']
    return commands_dict

def replace_placeholders(response):
    if "{date}" in response:
        response = response.replace("{date}", datetime.now().strftime("%B %d, %Y"))
    if "{time}" in response:
        response = response.replace("{time}", datetime.now().strftime("%I:%M %p"))
    return response

def calculate_expression(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return "I couldn't calculate that. Please try again."

def commands(commands_dict):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening... ask now...")
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            mytext = r.recognize_google(audio)
            mytext = mytext.lower()

            print(f"Recognized: {mytext}")

            for command, response in commands_dict.items():
                if command in mytext:
                    if '{calculate}' in response:
                        calculation = re.search(r'(\d+[\+\-\*/]\d+)', mytext)
                        if calculation:
                            result = calculate_expression(calculation.group())
                            response = response.replace('{calculate}', result)
                        else:
                            response = "I couldn't understand the calculation. Please try again."
                    elif '{query}' in response:
                        query = mytext.replace(command, "").strip()
                        response = response.replace("{query}", query)
                        if "search" in command:
                            webbrowser.open(f"https://www.google.com/search?q={query}")
                        elif "who is" in command:
                            webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
                    elif "play" in command:
                        song = mytext.replace("play", "").strip()
                        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
                        response = f"Playing {song} on YouTube."
                    else:
                        response = replace_placeholders(response)
                    speak(response)
                    return True

            speak("I didn't understand that. Can you please repeat?")
        return True 
    except sr.UnknownValueError:
        speak("I didn't catch that. Please try again.")
    except sr.RequestError as e:
        speak("I'm having trouble connecting to the service. Please check your internet.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An error occurred. Please try again.")
    return True  

speak("Welcome to the voice assistant!")
commands_dict = load_commands_from_csv('commands2.csv')

while True:
    if not commands(commands_dict):  
        break
