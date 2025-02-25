import tkinter as tk
from tkinter import simpledialog
from time import strftime
import requests  
import pytz
from datetime import datetime
from binance.client import Client

# Binance Credentials (Replace with your own keys)
API_KEY = ""
API_SECRET = ""
client = Client(API_KEY, API_SECRET)

# Constants
CITY = "Nairobi"
WEATHER_API_KEY = ""  # Replace with your API key

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
USER_NAME = simpledialog.askstring("Input", "Enter your name:") or "Guest"

# Function to get weather
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
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

def get_usd_to_kes_rate():
    try:
        API_KEY = ""  # Replace with your actual API key
        url = f"https://v6.exchangerate-api.com/v6//latest/USD"
        response = requests.get(url).json()
        return float(response["conversion_rates"]["KES"])
    except Exception as e:
        print("Error fetching USD to KES rate from Exchangerate API:", e)
        return 160  # Fallback rate



# Function to fetch Binance balances
def get_binance_balances():
    try:
        # 🔹 Fetch account balances
        account_info = client.get_account()
        balances = account_info["balances"]

        # 🔹 Filter non-zero balances
        owned_coins = {b["asset"]: float(b["free"]) for b in balances if float(b["free"]) > 0}

        # 🔹 Get estimated total in USD
        total_usd = 0
        balance_text = ""

        for coin, amount in owned_coins.items():
            symbol = f"{coin}USDT"
            try:
                price = float(client.get_symbol_ticker(symbol=symbol)["price"])
                usd_value = amount * price
                total_usd += usd_value
                balance_text += f"{coin}: {amount:.6f} ≈ ${usd_value:.2f}\n"
            except:
                balance_text += f"{coin}: {amount:.6f} (No USDT price found)\n"

        # 🔹 Convert to KES
        usd_to_kes = get_usd_to_kes_rate()
        total_kes = total_usd * usd_to_kes

        # 🔹 Update UI
        balance_label.config(text=balance_text)
        total_label.config(text=f"Total Balance: ${total_usd:.2f} | KES {total_kes:,.2f} (Rate: {usd_to_kes:.2f})")

    except Exception as e:
        total_label.config(text="Error fetching balance")
        print("Error fetching Binance balances:", e)

    root.after(2000, get_binance_balances)  # Refresh every 2 seconds




# Function to update all times
def update_time():
    global is_24_hour
    clock_label.config(text=strftime('%H:%M' if is_24_hour else '%I:%M %p'))
    
    newyork_label.config(text=f"New York\n{get_time('New York')}")
    london_label.config(text=f"London\n{get_time('London')}")
    tokyo_label.config(text=f"Tokyo\n{get_time('Tokyo')}")

    hour = int(strftime('%H'))
    greeting_label.config(text=f"Good {'Morning' if hour < 12 else 'Afternoon' if hour < 16 else 'Evening'}, {USER_NAME}!")
    date_label.config(text=strftime('%A, %B %d, %Y'))
    weather_label.config(text=get_weather())

    root.after(60000, update_time)

# Toggle between 12-hour and 24-hour format
def toggle_format():
    global is_24_hour
    is_24_hour = not is_24_hour
    update_time()

# Set up main window
root.deiconify()
root.title("My Assistant")
root.geometry("1600x800")
root.configure(bg="black")

is_24_hour = False

# Labels for greeting and weather
greeting_label = tk.Label(root, text="", font=("Helvetica", 24), fg="white", bg="black")
greeting_label.pack(pady=10)

# World Clocks
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

# Toggle Button
toggle_button = tk.Button(root, text="Toggle 24H/12H", command=toggle_format)
toggle_button.pack(pady=10)

# 🔹 Crypto Section (Bottom Left)
crypto_frame = tk.Frame(root, bg="black", padx=10, pady=10)
crypto_frame.pack(side="left", anchor="sw", padx=20, pady=20)

# Frame for Deposit & Withdraw (Side by Side)
top_crypto_frame = tk.Frame(crypto_frame, bg="black")
top_crypto_frame.pack(anchor="w", fill="x")

deposit_label = tk.Label(top_crypto_frame, text="Deposit (Crypto In):", font=("Helvetica", 16, "bold"), fg="green", bg="black")
deposit_label.pack(side="left", padx=20)

withdraw_label = tk.Label(top_crypto_frame, text="Withdraw (Crypto Out):", font=("Helvetica", 16, "bold"), fg="red", bg="black")
withdraw_label.pack(side="left", padx=20)

# Crypto Balances
balance_label = tk.Label(crypto_frame, text="Fetching balances...", font=("Helvetica", 14), fg="white", bg="black", justify="left")
balance_label.pack(anchor="w", pady=10)

# Total Balance (USD & KES)
total_label = tk.Label(crypto_frame, text="Total Balance: $0.00 | KES 0", font=("Helvetica", 16, "bold"), fg="white", bg="black")
total_label.pack(anchor="w", pady=10)

# Start Updates
update_time()
get_binance_balances()

# Run App
root.mainloop()
