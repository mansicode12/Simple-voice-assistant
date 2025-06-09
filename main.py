
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Sample music dictionary (replace with your actual musicLibrary)
music = {
    "hbl": "https://www.youtube.com/watch?v=8v-TWxPWIWc&pp=ygUIaHVtc2FmYXI%3D",
    "lover": "https://www.youtube.com/watch?v=-BjZmE2gtdo&pp=ygUSbG92ZXIgdGF5bG9yIHN3aWZ0",
    "darasal": "https://www.youtube.com/watch?v=uCMYzolEbO0&pp=ygUMZGFyYXNhbCBzb25n",
    "history": "https://www.youtube.com/watch?v=yjmp8CoZBIo&pp=ygUVaGlzdG9yeSBvbmUgZGlyZWN0aW9u"
}

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print(e)
        return None

# Function to get weather information
def get_weather(city):
    api_key = '175beb4eaf0336a1288c1b5a79242f8d'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if data['cod'] == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            speak(f"The weather in {city} is {weather_description}. The temperature is {temperature} degrees Celsius.")
        else:
            speak("Unable to fetch weather information.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather information at the moment.")

# Function to search news on Google News
def get_news_from_google():
    try:
        url = "https://news.google.com/news/rss"
        response = requests.get(url)
        if response.status_code == 200:
            speak("Here are the latest news headlines from Google News:")
            headlines = response.text.split('<title>')[1:]
            for headline in headlines[1:6]:  # Displaying top 5 headlines
                headline = headline.split('</title>')[0]
                speak(headline)
        else:
            speak("Sorry, I couldn't fetch news from Google News at the moment.")
    except Exception as e:
        speak("Sorry, I couldn't fetch news from Google News at the moment.")

# Function to handle user commands
def handle_command(command):
    if 'hello' in command:
        speak("Hello! How can I help you?")
    elif 'what is your name' in command:
        speak("I am a simple voice assistant.")
    elif 'what time is it' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif 'open google' in command:
        webbrowser.open('https://google.com')
        speak("Opening google")
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        speak("Opening youtube")
    elif 'open linkedin' in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening linkedin")
    elif command.lower().startswith("play"):
        try:
            song = command.lower().split(" ")[1]
            if song in music:
                link = music[song]
                webbrowser.open(link)
                speak(f"Now playing {song}")
            else:
                speak("No such song found in the playlist.")
        except IndexError:
            speak("Please specify which song to play.")
    elif 'weather in' in command:
        city = command.split("in")[1].strip()
        get_weather(city)
    elif 'news headlines' in command:
        get_news_from_google()
    elif 'stop' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't catch that.")

# Main program loop
if __name__ == "__main__":
    speak("Hello! How can I help you?")

    while True:
        command = recognize_speech()

        if command:
            handle_command(command)
