import tkinter as tk
from tkinter import Label, Entry, Button
from PIL import Image, ImageTk
import requests

def get_weather_data(city):
    api_key = 'd8a25fec9cf03bd39c8969dd05e1c67b'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

def update_weather():
    city = city_entry.get()
    weather_data = get_weather_data(city)
    if weather_data.get("main"):
        temp_celsius = weather_data["main"]["temp"]
        feels_like_celsius = weather_data["main"]["feels_like"]
        temp_fahrenheit = temp_celsius * 9/5 + 32
        feels_like_fahrenheit = feels_like_celsius * 9/5 + 32
        temp_kelvin = temp_celsius + 273.15
        feels_like_kelvin = feels_like_celsius + 273.15
        temperature_var.set(f"Temperature:\nCelsius: {temp_celsius:.2f}°C\nFahrenheit: {temp_fahrenheit:.2f}°F\nKelvin: {temp_kelvin:.2f}K")
        feels_like_var.set(f"Feels Like:\nCelsius: {feels_like_celsius:.2f}°C\nFahrenheit: {feels_like_fahrenheit:.2f}°F\nKelvin: {feels_like_kelvin:.2f}K")
    else:
        temperature_var.set("Error fetching data")
        feels_like_var.set("")

def resize_image(image):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    resized_image = image.resize((screen_width, screen_height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

root = tk.Tk()
root.title("Weather App")

image = Image.open("cloudy-weather.jpg")
photo = resize_image(image)
label_logo = Label(root, image=photo)
label_logo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

temperature_var = tk.StringVar()
temperature_var.set("Enter a city name and press 'Get Weather'")

feels_like_var = tk.StringVar()
feels_like_var.set("")

city_entry = Entry(root, font=("Helvetica", 24), justify="center")
city_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

get_weather_button = Button(root, text="Get Weather", command=update_weather, font=("Helvetica", 18))
get_weather_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

label_temp = Label(root, textvariable=temperature_var, font=("Helvetica", 24), bg="white", justify="center")
label_temp.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

label_feels_like = Label(root, textvariable=feels_like_var, font=("Helvetica", 24), bg="white", justify="center")
label_feels_like.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

root.mainloop()