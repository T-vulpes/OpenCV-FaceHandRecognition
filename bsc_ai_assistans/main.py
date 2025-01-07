import pyttsx3
import datetime
import wikipedia
import pywhatkit
import speech_recognition as sr

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  
    engine.say(command)
    engine.runAndWait()

def commands():
    r = sr.Recognizer()
    phonenumbers = {"gabi": "123456790", "zehra": "1111", "thomas": "222"}
    bankaccount = {"xx": "50000", "yy": "33332", "oo": "500"}

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening... ask now...")
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            mytext = r.recognize_google(audio)
            mytext = mytext.lower()

            print(f"Recognized: {mytext}")

            if "hello" in mytext and "how are you" in mytext:
                speak("I'm fine, thank you! How can I assist you today?")

            elif 'play' in mytext:
                mytext = mytext.replace('play', '')
                song_name = mytext.strip()
                specific_search = f"{song_name} official music video"
                speak(f"Searching for {song_name}")
                pywhatkit.playonyt(specific_search)

            elif 'date' in mytext:
                today = datetime.date.today()
                speak(f"Today's date is {today}")

            elif 'time' in mytext:
                time = datetime.datetime.now().strftime('%H:%M')
                speak(f"The time is {time}")

            if 'who is' in mytext:
                            person = mytext.replace('who is', '').strip()
                            try:
                                wikipedia.set_lang("en")  
                                info = wikipedia.summary(person, sentences=2)
                                speak(info)
                            except wikipedia.exceptions.DisambiguationError as e:
                                options = ', '.join(e.options[:5]) 
                                speak(f"There are multiple results for {person}. Did you mean: {options}?")
                            except wikipedia.exceptions.PageError:
                                speak(f"I couldn't find any information about {person}. Please try a different query.")
                            except Exception as e:
                                speak("An error occurred while fetching information from Wikipedia.")
                                print(f"Error: {e}")

            elif 'phone number' in mytext:
                for name in phonenumbers:
                    if name in mytext:
                        speak(f"{name}'s phone number is {phonenumbers[name]}")
                        break
                else:
                    speak("No matching phone number found.")

            elif "account number" in mytext:
                for bankname in bankaccount:
                    if bankname in mytext:
                        speak(f"{bankname}'s bank account number is {bankaccount[bankname]}")
                        break
                else:
                    speak("No matching bank account found.")

            elif 'exit' in mytext or 'quit' in mytext:
                speak("Exiting the program. Goodbye!")
                return False  

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
while True:
    if not commands():  
        break
