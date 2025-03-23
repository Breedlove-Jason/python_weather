import tkinter as tk
from tkinter import ttk
from weather_api import get_weather_data, parse_weather_data
from utils import load_svg_as_photoimage
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# --- Functions ---

def fetch_weather():
    """
    Retrieve weather data for either a city name or a postal code,
    based on the user's input.
    """
    location_input = city_entry.get().strip()
    if not location_input:
        # Clear fields if no input
        city_value.config(text="N/A")
        temp_value.config(text="N/A")
        feels_value.config(text="N/A")
        humid_value.config(text="N/A")
        desc_value.config(text="N/A")
        icon_label.config(image="")
        return

    weather_json = get_weather_data(location_input)
    if weather_json:
        parsed = parse_weather_data(weather_json)
        display_weather(parsed)
    else:
        # Show an error if data could not be fetched
        city_value.config(text="Error fetching data")
        temp_value.config(text="")
        feels_value.config(text="")
        humid_value.config(text="")
        desc_value.config(text="")
        icon_label.config(image="")

def display_weather(parsed_data):
    """
    Update the labels in the details frame with the parsed weather data.
    Show temperature in both Celsius and Fahrenheit.
    Place the icon to the right so it doesn't fall off the bottom.
    """
    # Extract fields
    city_str = parsed_data.get("city_name", "N/A")
    country_str = parsed_data.get("country", "N/A")

    temp_c = parsed_data.get("temp", "N/A")
    feels_c = parsed_data.get("feels_like", "N/A")
    humid_str = parsed_data.get("humidity", "N/A")
    desc_str = parsed_data.get("description", "N/A").capitalize()

    # Convert to Fahrenheit if temp is numeric
    temp_f = "N/A"
    feels_f = "N/A"
    if isinstance(temp_c, (int, float)):
        temp_f = round((temp_c * 9/5) + 32, 1)
    if isinstance(feels_c, (int, float)):
        feels_f = round((feels_c * 9/5) + 32, 1)

    # Update label texts
    city_value.config(text=f"{city_str}, {country_str}")
    temp_value.config(text=f"{temp_c}°C / {temp_f}°F")
    feels_value.config(text=f"{feels_c}°C / {feels_f}°F")
    humid_value.config(text=f"{humid_str}%")
    desc_value.config(text=desc_str)

    # Determine icon based on description
    icon_key = None
    desc_lower = desc_str.lower()
    if "clear" in desc_lower:
        icon_key = "clear"
    elif "cloud" in desc_lower:
        icon_key = "cloud"
    elif "rain" in desc_lower:
        icon_key = "rain"
    elif "snow" in desc_lower:
        icon_key = "snow"
    elif "thunder" in desc_lower:
        icon_key = "thunder"

    if icon_key:
        icon_img = load_svg_as_photoimage(icon_paths.get(icon_key), size=(64, 64))
        icon_label.config(image=icon_img)
        icon_label.image = icon_img
    else:
        icon_label.config(image="")

# --- Main Window Setup ---
# Use ttkbootstrap's Window with the superhero theme for rounded controls.
root = tb.Window(themename="superhero")
root.title("Weather App")
root.geometry("500x400")
root.resizable(False, False)

# Optional: Remove the following style configuration if you prefer the default bootstrap styling.
# (Note: ttkbootstrap comes with its own style, so mixing with manual ttk.Style() is not necessary.)
style = ttk.Style()
# Do not override the bootstrap theme with "clam":
# style.theme_use("clam")
# Base colors, fonts, and other style customizations can be set here if desired.

# --- Layout ---

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Header
header_label = ttk.Label(main_frame, text="Weather App", font=("Helvetica", 20, "bold"))
header_label.pack(pady=(0, 20))

# Input Frame using grid to align label, entry, and button
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=(0, 10), fill=tk.X)
input_frame.columnconfigure(1, weight=1)

city_label = ttk.Label(input_frame, text="Enter City or Zip:")
city_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

city_entry = ttk.Entry(input_frame, width=30)
city_entry.grid(row=0, column=1, sticky="ew")

# Create the button using ttkbootstrap's Button for rounded, orange appearance.
get_weather_button = tb.Button(
    input_frame,
    text="Get Weather",
    command=fetch_weather,
    bootstyle="warning"  # This gives an orange button in the superhero theme
)
get_weather_button.grid(row=0, column=2, padx=(10, 0))

# Results / Details Frame
details_frame = ttk.Frame(main_frame, padding="15")
details_frame.pack(fill=tk.X)

# Configure 3 columns to place icon in the rightmost column
details_frame.columnconfigure(0, weight=0)
details_frame.columnconfigure(1, weight=1)
details_frame.columnconfigure(2, weight=0)

# Row 0: City
city_header = ttk.Label(details_frame, text="City:", font=("Helvetica", 12, "bold"))
city_header.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
city_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
city_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

# Row 1: Temperature
temp_header = ttk.Label(details_frame, text="Temperature:", font=("Helvetica", 12, "bold"))
temp_header.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
temp_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
temp_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

# Row 2: Feels Like
feels_header = ttk.Label(details_frame, text="Feels like:", font=("Helvetica", 12, "bold"))
feels_header.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
feels_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
feels_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

# Row 3: Humidity
humid_header = ttk.Label(details_frame, text="Humidity:", font=("Helvetica", 12, "bold"))
humid_header.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
humid_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
humid_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

# Row 4: Description
desc_header = ttk.Label(details_frame, text="Description:", font=("Helvetica", 12, "bold"))
desc_header.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
desc_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
desc_value.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

# Icon in the rightmost column, spanning multiple rows
icon_label = ttk.Label(details_frame)
icon_label.grid(row=0, column=2, rowspan=5, padx=(10, 0), pady=5, sticky="n")

# Weather Icon Paths
icon_paths = {
    "clear": "./icons/sun-sharp-solid.svg",
    "snow": "./icons/snowflake-sharp-solid.svg",
    "rain": "./icons/umbrella-sharp-solid.svg",
    "cloud": "./icons/cloud-sharp-solid.svg",
    "thunder": "./icons/bolt-sharp-solid.svg"
}

root.mainloop()
