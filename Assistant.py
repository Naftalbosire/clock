import tkinter as tk
from tkinter import simpledialog
from time import strftime
import requests  
import pytz
import speedtest
from datetime import datetime
from binance.client import Client

print("🔹 Assistant is running...")  # New line


# Binance Credentials (Replace with your own keys)
API_KEY = "QMCFymSe2WsCsG1ZJrsBXXbwB4jSP6yLki1P7ATRRazhY9L02YslbaPmjp2kVrsP"
API_SECRET = "QGrj1DWAZWnbPb3nfeEFHAxQZlGbiYIhizYniCIy69rRwfKFgdKrBPUpUvgRpDZI"
client = Client(API_KEY, API_SECRET)

# Constants
CITY = "Nairobi"
WEATHER_API_KEY = "b050f35226cff1614e8c65dfea0cff85"  # Replace with your API key

# Timezones for world clocks
TIMEZONES = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
}

# Create root window
root = tk.Tk()
root.withdraw()  


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
        API_KEY = "IH996TCU6QIXW640"  # Replace with your actual API key
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=KES&apikey={API_KEY}"
        response = requests.get(url).json()
        return float(response["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except Exception as e:
        print("Error fetching USD to KES rate from Alpha Vantage API:", e)
        return 129  # Fallback rate

# Function to fetch Binance balances
def get_binance_balances():
    try:
        # Fetch account balancesx
        account_info = client.get_account()
        balances = account_info["balances"]

        # Filter non-zero balances
        owned_coins = {b["asset"]: float(b["free"]) for b in balances if float(b["free"]) > 0}

        # If no balance, show message
        if not owned_coins:
            balance_label.config(text="You have no crypto holdings.")
            total_label.config(text="Total Balance: $0.00 | KES 0")
            return

        # Get estimated total in USD
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

        # Convert to KES
        usd_to_kes = get_usd_to_kes_rate()
        total_kes = total_usd * usd_to_kes

        # Ensure balance and total labels are updated correctly
        balance_label.config(text=balance_text, fg="white", font=("Helvetica", 14))
        total_label.config(
            text=f"Total Balance: ${total_usd:.2f} | KES {total_kes:,.2f} (Rate: {usd_to_kes:.2f})",
            fg="yellow",
            font=("Helvetica", 16, "bold")
        )

    except Exception as e:
        total_label.config(text="Error fetching balance", fg="red")
        print("Error fetching Binance balances:", e)

    root.after(30000, get_binance_balances) 

# check internet speed

def check_internet_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # Measure speeds
        download_speed = st.download() / 1_000_000  
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        
        # Display speeds if connected
        internet_label.config(text=f"📶 {download_speed:.2f} Mbps ↓ | {upload_speed:.2f} Mbps ↑", fg="green")
    
    except Exception as e:
        print("Speedtest Error:", e)  # Debugging log
        internet_label.config(text="❌", fg="red")  # Show ❌ if there's an error
    
    root.after(10_000, check_internet_speed)


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

    root.after(59000, update_time)

# Toggle between 12-hour and 24-hour format
def toggle_format():
    global is_24_hour
    is_24_hour = not is_24_hour
    update_time()

# Set up main window
root.deiconify()
root.title("Assistant")
root.geometry("1600x800")
root.configure(bg="black")

is_24_hour = False

# Labels for greeting and weather
greeting_label = tk.Label(root, text="", font=("Helvetica", 24), fg="white", bg="black")
greeting_label.pack(pady=10)

# internet connection
internet_label = tk.Label(root, text="Checking Internet...", font=("Helvetica", 18), fg="yellow", bg="black")
internet_label.pack()


# World Clocks
world_clock_frame = tk.Frame(root, bg="black")
world_clock_frame.pack(pady=20, fill="x", expand=True)

newyork_label = tk.Label(world_clock_frame, text="", font=("Helvetica", 40, "bold"), fg="white", bg="black")
newyork_label.pack(side="left", expand=True)

london_label = tk.Label(world_clock_frame, text="", font=("Helvetica", 40, "bold"), fg="white", bg="black")
london_label.pack(side="left", expand=True)

tokyo_label = tk.Label(world_clock_frame, text="", font=("Helvetica", 40, "bold"), fg="white", bg="black")
tokyo_label.pack(side="left", expand=True)

# Main Clock
clock_label = tk.Label(root, text="", font=("Helvetica", 150, "bold"), fg="white", bg="black")
clock_label.pack()

date_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
date_label.pack()

weather_label = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
weather_label.pack()

# Toggle Button
toggle_button = tk.Button(root, text="Toggle 24H/12H", command=toggle_format)
toggle_button.pack(pady=10)

# Crypto Balances Section
crypto_frame = tk.Frame(root, bg="black", padx=20, pady=10)  # Reduce padding
crypto_frame.pack(side="left", anchor="sw", padx=20, pady=10)  # Moves it slightly up


# Frame for Deposit & Withdraw
top_crypto_frame = tk.Frame(crypto_frame, bg="black")
top_crypto_frame.pack(anchor="w", fill="x")

deposit_label = tk.Label(top_crypto_frame, text="Deposit (Crypto In): ******", 
                         font=("Helvetica", 16, "bold"), fg="green", bg="black")
deposit_label.pack(side="left", padx=20)

withdraw_label = tk.Label(top_crypto_frame, text="Withdraw (Crypto Out): ******", 
                          font=("Helvetica", 16, "bold"), fg="red", bg="black")
withdraw_label.pack(side="left", padx=20)

# Crypto Balances
balance_label = tk.Label(crypto_frame, text="Fetching balances...", font=("Helvetica", 14), fg="white", bg="black", justify="left")
balance_label.pack(anchor="w", pady=10)

# Total Balance (USD & KES)
total_label = tk.Label(crypto_frame, text="Total Balance: $0.00 | KES 0", font=("Helvetica", 16, "bold"), fg="white", bg="black", anchor="w")
total_label.pack(fill="x", padx=20, pady=10)

# Start Updates
update_time()
get_binance_balances()
check_internet_speed()
# get_btc_price()



# Run App
root.mainloop()
