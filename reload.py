import sys
import os
import importlib
import time

# Add the current script directory to Python's module search path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

import Assistant  # Import assistant.py

def reload_modules():
    """Reloads the assistant module without restarting the script."""
    importlib.reload(Assistant)
    print("🔄 Assistant updated!")

while True:
    try:
        reload_modules()  # Reload the assistant module
        time.sleep(2)  # Check for changes every 2 seconds
    except KeyboardInterrupt:
        print("Stopping hot reload...")
        break
