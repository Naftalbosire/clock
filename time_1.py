import tkinter as tk
from tkinter import simpledialog
from time import strftime
import requests  
import pytz
from datetime import datetime

# Constants
CITY = "Nairobi"
API_KEY = "_____"  # Replace with your API key

# Timezones for world clocks
TIMEZONES = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
}

# Create root window
root = tk.Tk()
root.withdraw()  # Hide until name is entered

# Ask for user name
USER_NAME = simpledialog.askstring("Input", "Enter your name:")
USER_NAME = USER_NAME if USER_NAME else "Guest"

# Function to get weather
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        weather_desc = response["weather"][0]["description"].title()
        return f"{CITY}: {temp}°C, {weather_desc}"
    except:
        return "Weather data unavailable"

# Function to get time in a given city
def get_time(city):
    tz = pytz.timezone(TIMEZONES[city])
    return datetime.now(tz).strftime('%H:%M' if is_24_hour else '%I:%M %p')

# Function to update all times
def update_time():
    global is_24_hour

    # Update main clock
    current_time = strftime('%H:%M' if is_24_hour else '%I:%M %p')
    clock_label.config(text=current_time)

    # Update world clocks above the main clock
    newyork_label.config(text=f"New York\n{get_time('New York')}")
    london_label.config(text=f"London\n{get_time('London')}")
    tokyo_label.config(text=f"Tokyo\n{get_time('Tokyo')}")

    # Greeting message
    hour = int(strftime('%H'))
    if 5 <= hour < 12:
        greeting = f"Good Morning, {USER_NAME}!"
    elif 12 <= hour < 18:
        greeting = f"Good Afternoon, {USER_NAME}!"
    else:
        greeting = f"Good Evening, {USER_NAME}!"
    
    greeting_label.config(text=greeting)
    date_label.config(text=strftime('%A, %B %d, %Y'))
    weather_label.config(text=get_weather())

    # Refresh every minute
    root.after(60000, update_time)

# Toggle between 12-hour and 24-hour format
def toggle_format():
    global is_24_hour
    is_24_hour = not is_24_hour
    update_time()

# Set up main window
root.deiconify()
root.title("World Clock")
root.geometry("1600x800")
root.configure(bg="black")

is_24_hour = False

# Labels for greeting and weather
greeting_label = tk.Label(root, text="", font=("Helvetica", 24), fg="white", bg="black")
greeting_label.pack(pady=10)

# 🔹 World Clocks (Above the main clock)
world_clock_frame = tk.Frame(root, bg="black")
world_clock_frame.pack(pady=20)

newyork_label = tk.Label(world_clock_frame, text="", font=("Helvetica", 40, "bold"), fg="white", bg="black")
newyork_label.grid(row=0, column=0, padx=40)

london_label = tk.Label(world_clock_frame, text="", font=("Helvetica", 40, "bold"), fg="white", bg="black")
london_label.grid(row=0, column=1, padx=40)

tokyo_label = tk.Label(world_clock_frame, text="", font=("Helvetica", 40, "bold"), fg="white", bg="black")
tokyo_label.grid(row=0, column=2, padx=40)

# Main Clock
clock_label = tk.Label(root, text="", font=("Helvetica", 200, "bold"), fg="white", bg="black")
clock_label.pack()

date_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
date_label.pack()

weather_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
weather_label.pack()

# Buttons to toggle features
toggle_button = tk.Button(root, text="Toggle 24H/12H", command=toggle_format)
toggle_button.pack(pady=10)

# Start the clock
update_time()

# Run the application
root.mainloop()
