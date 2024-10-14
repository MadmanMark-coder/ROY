import speech_recognition as sr 
import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup
import re
import random

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input and recognize it
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {query}")
            return query.lower()
        except Exception:
            print("Sorry, I didn't catch that. Please repeat...")
            return "none"

# Function to get the current time
def tell_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    return f"The time is {time}."

# Function to search the web and return a short answer
def search_web(query):
    try:
        # Format query for Google search
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        response = requests.get(search_url)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract a short answer (simple example)
            answer = ""
            for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
                # Take only the first relevant answer
                answer = g.get_text()
                break

            return answer.strip() if answer else "No answer found."
        else:
            return "I couldn't fetch data from the internet."
    except requests.RequestException:
        return "There was an error connecting to the internet."

# Function to calculate math expressions
def calculate_math(query):
    try:
        query = re.sub(r'[^0-9+\-*/().]', '', query)  # Remove unwanted characters
        result = eval(query)
        return f"The result is: {result}."
    except Exception:
        return "I couldn't understand the math problem."

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call cheese that isn't yours? Nacho cheese!"
    ]
    return random.choice(jokes)

# Function to generate a response based on user queries
def generate_response(query):
    if "time" in query:
        return tell_time()
    elif re.match(r'^\d+(\s*[\+\-\*/]\s*\d+)+$', query):  # Check if the query is a math expression
        return calculate_math(query)
    elif "joke" in query:
        return tell_joke()
    elif "stop" in query or "exit" in query:
        return "Goodbye! Have a great day!"
    else:
        # Perform a web search for answers to other questions
        return search_web(query)

# Main function to handle commands
def ai_voice_assistant():
    speak("Hello! I am ROY., your AI voice assistant. Made by MARK,how can i help you out")
    
    while True:
        query = take_command()
        
        if query == "none":
            continue
        
        response = generate_response(query)
        
        # Speak the response
        speak(response)
        
        # Exit if the user says "stop" or "exit"
        if "stop" in query or "exit" in query:
            break

# Run the AI Voice Assistant
if __name__ == "__main__":
    ai_voice_assistant()       