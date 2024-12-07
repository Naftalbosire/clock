import tkinter as tk
from time import strftime
from tkinter import Canvas

# Update this with your name
USER_NAME = "Naftal"

def update_time():
    # Get the current time (hour and minute only)
    current_time = strftime('%I:%M %p')
    clock_label.config(text=current_time)
    
    # Update greeting based on the time of day
    hour = int(strftime('%H'))
    if 5 <= hour < 12:
        greeting = f"Good Morning, {USER_NAME}!"
    elif 12 <= hour < 18:
        greeting = f"Good Afternoon, {USER_NAME}!"
    else:
        greeting = f"Good Evening, {USER_NAME}!"
    greeting_label.config(text=greeting)
    
    # Schedule the function to update every minute
    clock_label.after(1000, update_time)

# Initialize the main app window
root = tk.Tk()
root.title("Flip Clock")
root.geometry("1600x800")  # Adjust screen size as needed
root.configure(bg="black")

# Add greeting label
greeting_label = tk.Label(root, text="", font=("Helvetica", 24), fg="white", bg="black")
greeting_label.pack(pady=10)

# Add clock label
clock_label = tk.Label(root, text="", font=("Helvetica", 240, "bold"), fg="white", bg="black")
clock_label.pack(expand=True)

# Update the time and greetings
update_time()

# Run the application
root.mainloop()
