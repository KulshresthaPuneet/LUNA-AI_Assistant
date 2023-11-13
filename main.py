import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import random
import cv2
import sys
import pyautogui
import time
import operator
import requests
from googletrans import Translator, LANGUAGES
from geopy.geocoders import Nominatim
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning, I am Luna. I am here to assist you.")
        speak("Good Morning, I am Luna. I am here to assist you.")
    elif hour >= 12 and hour < 18:
        print("Good Afternoon, I am Luna. I am here to assist you.")
        speak("Good Afternoon, I am Luna. I am here to assist you.")
    else:
        print("Good Evening, I am Luna. I am here to assist you.")
        speak("Good Evening, I am Luna. I am here to assist you.")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=10)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        query = query.replace("Luna", "")
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please")
        return "None"
    return query


def calculate_expression(expression):
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        'x': operator.mul,
    }

    parts = expression.split()
    if len(parts) != 3:
        return "Invalid expression"

    operand1, operator_symbol, operand2 = parts

    try:
        result = operators[operator_symbol](float(operand1), float(operand2))
        return result
    except (ValueError, ZeroDivisionError) as e:
        return "Error: " + str(e)


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid=ed5e37c9d02774e8aa03d9810a6f7663&units=metric"

    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        mai_data = weather_data["main"]
        temperature = mai_data["temp"]
        humidity = mai_data["humidity"]
        weather_info = weather_data["weather"][0]["description"]

        weather_report = f"The weather in {city} today is {weather_info}. "
        weather_report += f"The temperature is {temperature}°C, and the humidity is {humidity}%."
        return weather_report
    else:
        return "City not found."


def translate_command(command, target_language='en'):
    translator = Translator()
    try:
        translated = translator.translate(
            command, src='en', dest=target_language)
        return translated.text
    except Exception as e:
        return str(e)


if __name__ == "__main__":

    wishMe()

    while True:

        query = takeCommand().lower()

        if "Luna" and "who are you" in query:
            print(
                "My name is Luna. Stands for Logical Understanding and Navigational Assistant.")
            speak(
                "My name is Luna. Stands for Logical Understanding and Navigational Assistant.")

        elif "Luna" and "who created you" in query:
            print("My creator is The SHIPP")
            speak("My creator is The SHIPP")

        elif "Luna" and "what is the weather today" in query:
            speak("Please specify the city for the weather report.")
            city = takeCommand().lower()
            weather_report = get_weather(city)
            print(weather_report)
            speak(weather_report)

        elif "Luna" and "translate" in query:
            target_language = query.split("to")[-1].strip()

            if target_language:
                speak("What should I translate?")
                command_to_translate = takeCommand()
                translated_command = translate_command(
                    command_to_translate, target_language)
                print(f"Translated command: {translated_command}")
                speak(f"Translated command: {translated_command}")
            else:
                speak("Please specify the target language for translation.")

        elif "Luna" and "tell me a joke" in query:
            joke_url = "https://official-joke-api.appspot.com/random_joke"
            response = requests.get(joke_url)
            if response.status_code == 200:
                joke_data = response.json()
                joke_setup = joke_data["setup"]
                joke_punchline = joke_data["punchline"]
                joke = f"{joke_setup} {joke_punchline}"
                print(joke)
                speak(joke)

        elif "Luna" and "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(5)
                if k == 27:
                    break
                elif k == ord('c'):
                    speak("tell me a name for the file")
                    img_name = takeCommand().lower()
                    cv2.imwrite(f'{img_name}.jpg', img)
                    print("Image captured and saved")
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "Luna" and "take a screenshot" in query:
            speak("tell me a name for the file")
            name = takeCommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot Saved")

        elif "Luna" and "calculate" in query:
            expression = query.replace("calculate", "")
            result = calculate_expression(expression)
            print("The result is: " + str(result))
            speak("The result is: " + str(result))

        elif "Luna" and "my ip address" in query:
            speak("checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak("your ip address is")
                speak(ipAdd)
            except Exception as e:
                speak("Network is weak, please try again later")

        elif "Luna" and "create a folder" in query:
            speak("Sure, please specify the folder name.")
            folder_name = takeCommand()
            speak("Please specify the folder path")
            fold_path = takeCommand()
            if folder_name != "None":
                folder_path = os.path.join(
                    f"C:\\Users\\One Drive\\{fold_path}", folder_name)
                try:
                    os.mkdir(folder_path)
                    print(f"Folder '{folder_name}' created at '{folder_path}'")
                    speak(f"Folder '{folder_name}' created at '{fold_path}'")
                except OSError as e:
                    print(f"Error creating folder: {e}")
                    speak(f"Sorry, there was an error creating the folder.")
            else:
                speak("Sorry, I couldn't understand the folder name.")
                
        elif "Luna" and "restaurants near me" in query:
            try:
                geolocator = Nominatim(user_agent="restaurant_finder")
                location = geolocator.geocode("Rewa Engineering College", "India") 
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    nominatim_url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
                    response = requests.get(nominatim_url)
                    location_data = response.json()

                    if "address" in location_data:
                        city = location_data["address"].get("city", "")
                        country = location_data["address"].get("country", "")

                        search_query = "restaurants"
                        search_url = f"https://nominatim.openstreetmap.org/search?format=json&q={search_query}&city={city}&country={country}"
                        response = requests.get(search_url)
                        restaurant_data = response.json()

                        if restaurant_data:
                            restaurant_info = ""
                            for i, restaurant in enumerate(restaurant_data):
                                name = restaurant.get("display_name", "Name not available")
                                restaurant_info += f"{i + 1}. {name}\n"

                            print("Here are some nearby restaurants:\n")
                            print(restaurant_info)
                            speak("Here are some nearby restaurants:\n")
                            speak(restaurant_info)

                        else:
                            print("No restaurants found nearby.")
                            speak("I'm sorry, I couldn't find any restaurants nearby.")

                    else:
                        print("Location data not available.")
                        speak("I couldn't determine your location.")

                else:
                    print("Location not found.")
                    speak("I couldn't determine your location.")

            except Exception as e:
                print(f"Error: {e}")
                speak("Sorry, there was an error while fetching restaurant information.")


        elif "Luna" and "tell me the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")

        elif "Luna" and "flip a coin" in query:
            result = random.randint(0, 1)
            if result == 0:
                print("It's heads!")
                speak("It's heads!")
            else:
                print("It's tails!")
                speak("It's tails!")

        elif "Luna" and "open google" in query:
            webbrowser.open_new_tab("google.com")

        elif "Luna" and "open youtube" in query:
            webbrowser.open_new_tab("youtube.com")

        elif "Luna" and "open notepad" in query:
            npath = "C:\WINDOWS\system32\\notepad.exe"
            os.startfile(npath)

        elif "Luna" and "open settings" in query:
            os.startfile("ms-settings:")

        elif "Luna" and "open command prompt" in query:
            os.system("start cmd")

        elif "Luna" and "open paint" in query:
            os.startfile(
                r"C:\Users\Sumit\AppData\Local\Microsoft\WindowsApps\mspaint.exe")

        elif "Luna" and "open new window" in query:
            pyautogui.hotkey('ctrl', 'n')

        elif "Luna" and "close youtube" in query:
            os.system("taskkill /f /im msedge.exe")
            os.system("taskkill /f /im chrome.exe")

        elif "Luna" and "close browser" in query:
            os.system("taskkill /f /im msedge.exe")

        elif "Luna" and "close chrome" in query:
            os.system("taskkill /f /im chrome.exe")

        elif "Luna" and "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")

        elif "Luna" and "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")

        elif "Luna" and "close paint" in query:
            os.system("taskkill /f /im mspaint.exe")

        elif "Luna" and "close music" in query:
            os.system("taskkill /f /im vlc.exe")

        elif "Luna" and "close movie" in query:
            os.system("taskkill /f /im vlc.exe")

        elif "Luna" and "search in google" in query:
            speak("What should I search?")
            qry = takeCommand().lower()
            webbrowser.open_new_tab(f"{qry}")
            results = wikipedia.summary(qry, sentences=2)
            print(results)
            speak(results)

        elif "Luna" and "search in youtube" in query:
            speak("What would you like to watch?")
            qrry = takeCommand().lower()
            webbrowser.open_new_tab(
                f"www.youtube.com/results?search_query={qrry}")

        elif "Luna" and "play music" in query:
            music_dir = r"C:\Users\Sumit\Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))

        elif "Luna" and "play a song by" in query:
            song = query.replace("play a song by", "")
            wk.playonyt(song)

        elif "Luna" and "play" and "youtube" in query:
            vid = query.replace("play", "")
            wk.playonyt(vid)

        elif "Luna" and "type" in query:
            query = query.replace("type", "")
            pyautogui.typewrite(f"{query}", 0.1)

        elif "Luna" and "undo" in query:
            pyautogui.hotkey('ctrl', 'z')

        elif "Luna" and "maximize window" in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('x')

        elif "Luna" and "minimise window" in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('n')

        elif "Luna" and "enter" in query:
            pyautogui.press('enter')

        elif "Luna" and "shut down the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "Luna" and "hibernate the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "Luna" and "go to sleep" in query:
            speak("I am switching off")
            sys.exit()

        elif "Luna" and "volume up" in query:
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")

        elif "Luna" and "volume down" in query:
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")

        elif "Luna" and "what is" in query:
            print("Searching Wikipedia")
            speak("Searching Wikipedia")
            query = query.replace("what is", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "Luna" and "who is" in query:
            speak("Searching Wikipedia")
            query = query.replace("who is", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
