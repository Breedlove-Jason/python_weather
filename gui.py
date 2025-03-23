import tkinter as tk
from tkinter import ttk
from weather_api import get_weather_data, parse_weather_data
from utils import load_svg_as_photoimage

# --- Functions ---

def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        result_label.config(text="Please enter a city name.")
        return
    weather_json = get_weather_data(city)
    if weather_json:
        parsed = parse_weather_data(weather_json)
        display_weather(parsed)
    else:
        result_label.config(text="Error fetching weather.")

def display_weather(parsed_data):
    # Access dictionary values rather than unpacking keys
    city_name = parsed_data.get("city_name", "N/A")
    country = parsed_data.get("country", "N/A")
    temp = parsed_data.get("temp", "N/A")
    feels_like = parsed_data.get("feels_like", "N/A")
    humidity = parsed_data.get("humidity", "N/A")
    description = parsed_data.get("description", "N/A")

    # Format the weather display text
    text = (f"City: {city_name}, {country}\n"
            f"Temperature: {temp}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Description: {description.capitalize()}")
    result_label.config(text=text)

    # Determine the icon to display based on the description.
    icon_key = None
    if "clear" in description.lower():
        icon_key = "clear"
    elif "cloud" in description.lower():
        icon_key = "cloud"
    elif "rain" in description.lower():
        icon_key = "rain"
    elif "snow" in description.lower():
        icon_key = "snow"
    elif "thunder" in description.lower():
        icon_key = "thunder"

    if icon_key:
        icon_img = load_svg_as_photoimage(icon_paths.get(icon_key), size=(64, 64))
        icon_label.config(image=icon_img)
        icon_label.image = icon_img
    else:
        icon_label.config(image='')

# --- Main Window Setup ---

root = tk.Tk()
root.title("Weather App")
root.geometry("500x400")
root.resizable(False, False)

# Configure the style for a modern, dark theme.
style = ttk.Style()
style.theme_use("clam")  # 'clam' theme allows for more customization

# Set a dark background and white foreground for a sleek look.
style.configure("TFrame", background="#2C3E50")
style.configure("TLabel", background="#2C3E50", foreground="white", font=("Helvetica", 12))
style.configure("Header.TLabel", background="#2C3E50", foreground="white", font=("Helvetica", 20, "bold"))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), padding=6)
# Note: TButton backgrounds may depend on the OS. The 'clam' theme is more receptive to customizations.

# --- Layout Setup ---

# Main container frame with padding
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Header
header_label = ttk.Label(main_frame, text="Weather App", style="Header.TLabel")
header_label.pack(pady=(0, 20))

# Input Frame for City Entry
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=(0, 10), fill=tk.X)
city_label = ttk.Label(input_frame, text="Enter City:")
city_label.pack(side=tk.LEFT, padx=(0, 10))
city_entry = ttk.Entry(input_frame, width=30)
city_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Get Weather Button
get_weather_button = ttk.Button(main_frame, text="Get Weather", command=fetch_weather)
get_weather_button.pack(pady=(0, 20))

# Result Display Frame
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True)
result_label = ttk.Label(result_frame, text="", anchor="center", justify=tk.CENTER)
result_label.pack(pady=(10, 10))

# Weather Icon Display
icon_label = ttk.Label(result_frame)
icon_label.pack(pady=(10, 10))

# Icon paths dictionary for weather icons
icon_paths = {
    "clear": "./icons/sun-sharp-solid.svg",
    "snow": "./icons/snowflake-sharp-solid.svg",
    "rain": "./icons/umbrella-sharp-solid.svg",
    "cloud": "./icons/cloud-sharp-solid.svg",
    "thunder": "./icons/bolt-sharp-solid.svg"
}

root.mainloop()
