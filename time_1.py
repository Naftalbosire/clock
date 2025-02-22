import tkinter as tk
from tkinter import simpledialog
from time import strftime
import requests  

CITY = "Nairobi"
API_KEY = "_____" 

# Create the root window first (needed for dialogs)
root = tk.Tk()
root.withdraw()  # Hide main window until we get the name

# Ask for the user's name using a Tkinter dialog
USER_NAME = simpledialog.askstring("Input", "Enter your name:")

# If the user cancels, set a default name
if not USER_NAME:
    USER_NAME = "Guest"

# Function to get weather data
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        weather_desc = response["weather"][0]["description"].title()
        return f"{CITY}: {temp}°C, {weather_desc}"
    except:
        return "Weather data unavailable"

# Function to update time, greeting, and weather
def update_time():
    global is_24_hour
    
    current_time = strftime('%H:%M' if is_24_hour else '%I:%M %p')
    clock_label.config(text=current_time)
    
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
    clock_label.after(60000, update_time)

# Toggle between 12-hour and 24-hour format
def toggle_format():
    global is_24_hour
    is_24_hour = not is_24_hour
    update_time()

# Change background color
def change_bg_color(color):
    root.configure(bg=color)
    greeting_label.configure(bg=color)
    clock_label.configure(bg=color)
    date_label.configure(bg=color)
    weather_label.configure(bg=color)

# Change font
def change_font(font):
    clock_label.config(font=(font, 240, "bold"))

# Set up main window
root.deiconify()  # Show the main window
root.title("Flip Clock")
root.geometry("1600x800")
root.configure(bg="black")

is_24_hour = False  # Default to 12-hour format

# Labels
greeting_label = tk.Label(root, text="", font=("Helvetica", 24), fg="white", bg="black")
greeting_label.pack(pady=10)
clock_label = tk.Label(root, text="", font=("Helvetica", 240, "bold"), fg="white", bg="black")
clock_label.pack(expand=True)
date_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
date_label.pack()
weather_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
weather_label.pack()

# Buttons to toggle features
toggle_button = tk.Button(root, text="Toggle 24H/12H", command=toggle_format)
toggle_button.pack(pady=10)
color_button = tk.Button(root, text="Change BG Color", command=lambda: change_bg_color("darkblue"))
color_button.pack(pady=10)
font_button = tk.Button(root, text="Change Font", command=lambda: change_font("Courier"))
font_button.pack(pady=10)

# Start the clock
update_time()

# Run the application
root.mainloop()