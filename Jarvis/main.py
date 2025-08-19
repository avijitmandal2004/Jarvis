import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
import requests 
import wikipedia
from openai import OpenAI
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d093053d72bc4024899159804e0e67d"
OPENAI_API_KEY = ("ssk-proj-9rYSUkNf_bMzvaVNQmZRG9uub7vsrgtBKbfWx0WhAy4Ani-3btGay1oTPW6EageMwrbTdAkth1T3BlbkFJlDxLx6E26H1EAlWCqMC5bc-pLYytSAHv3gFZcZuAD9vCwi0StL9cwXvasLXEtYJi4912MMekUA")

def speak(text):
    engine.say(text)
    engine.runAndWait()
def aiprocess(command):
    client = OpenAI(api_key="ssk-proj-9rYSUkNf_bMzvaVNQmZRG9uub7vsrgtBKbfWx0WhAy4Ani-3btGay1oTPW6EageMwrbTdAkth1T3BlbkFJlDxLx6E26H1EAlWCqMC5bc-pLYytSAHv3gFZcZuAD9vCwi0StL9cwXvasLXEtYJi4912MMekUA")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant skilled in general tasks like Alexa and Google Cloud."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message["content"]



    

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        found = False
        for title, link in musiclibrary.music.items():
            if song == title.lower():
                webbrowser.open(link)
                found = True
                break
        if not found:
            speak("I don't have that song in my library.")
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles:
                    speak(article['title'])
            else:
                speak("I couldn't find any news right now.")
        elif r.status_code == 401:
            speak("Your NewsAPI key is invalid.")
        else:
            speak(f"Failed to fetch news. Status code: {r.status_code}")

    elif "tell me about" in c.lower():
        try:
            topic = c.lower().replace("tell me about", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Your query is too broad. Maybe you meant {e.options[0]}?")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find anything on Wikipedia.")
        except Exception as e:
            speak("Something went wrong with Wikipedia.")

   
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    wake_words = ["jarvis", "jarvish", "service"]
    recognizer = sr.Recognizer()   
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)
                word = recognizer.recognize_google(audio)

            if any(w in word.lower() for w in wake_words):
                speak("Yes!")
                with sr.Microphone() as source:
                    print("Jarvis Active...!")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                if "exit" in command.lower():
                    speak("Goodbye Avijit! See you soon.")
                    break
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Network error.")
        except Exception as e:
            print(f"Error: {e}")
