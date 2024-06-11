import speech_recognition as sr
import pyttsx3
import tkinter as tk
from datetime import datetime
import os
import webbrowser

recognizer = sr.Recognizer()

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio)
            print("User said:", query)
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""

def handle_query(query):
    response = ""
    if query:
        if "hello" in query.lower():
            response = "Hello! How can I help you?"
        elif "goodbye" in query.lower():
            response = "Goodbye!"
        elif "how are you" in query.lower():
            response = "I am fine. How can I help you?"
        elif "date" in query.lower():
            date = datetime.now().strftime("%A, %B %d, %Y")
            response = "Today's date is " + date
        elif "day" in query.lower():
            day = datetime.now().strftime("%A")
            response = "Today is " + day
        elif "time" in query.lower():
            time = datetime.now().strftime("%I:%M %p")
            response = "The time is " + time
        elif "open" in query.lower():
            app_name = query.lower().replace("open", "").strip()
            try:
                os.system(f"start {app_name}.exe")
                response = f"Opened {app_name}"
            except Exception as e:
                response = f"Could not open {app_name}: {e}"
        elif "search" in query.lower():
            search_query = query.lower().replace("search", "").strip()
            url = "https://www.google.com/search?q=" + "+".join(search_query.split())
            webbrowser.open(url)
            response = f"Here are the search results for {search_query}"
        else:
            response = "I'm sorry, I didn't understand that."

        speak(response)

        response_label.config(text=response)

window = tk.Tk()
window.title("Voice Assistant")

mic_logo = tk.PhotoImage(file="mic.png").subsample(3, 3)
logo_label = tk.Label(window, image=mic_logo)
logo_label.pack()
logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def on_voice_click():
    query = listen()
    handle_query(query)

def on_text_submit():
    query = text_entry.get()
    handle_query(query)
    text_entry.delete(0, tk.END)

voice_button = tk.Button(window, text="Listen and Respond", command=on_voice_click)
voice_button.pack()

text_entry = tk.Entry(window)
text_entry.pack()

text_button = tk.Button(window, text="Submit Text", command=on_text_submit)
text_button.pack()

response_label = tk.Label(window, text="", wraplength=300)
response_label.pack()

window.mainloop()