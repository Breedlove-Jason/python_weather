import tkinter as tk
from tkinter import ttk
from weather_api import (
    get_weather_data,
    get_forecast_data,
    parse_weather_data,
    parse_forecast_data
)
from utils import load_svg_as_photoimage, get_weather_icon
import ttkbootstrap as tb
from datetime import datetime

# --- Functions ---

def fetch_weather():
    """
    Retrieve current weather and forecast data for a given city name or zip code.
    """
    location_input = city_entry.get().strip()
    if not location_input:
        # Clear current weather fields
        city_value.config(text="N/A")
        temp_value.config(text="N/A")
        feels_value.config(text="N/A")
        humid_value.config(text="N/A")
        desc_value.config(text="N/A")
        icon_label.config(image="")
        # Also clear any forecast cards
        for widget in forecast_frame.winfo_children():
            widget.destroy()
        return

    # Current weather
    weather_json = get_weather_data(location_input)
    if weather_json:
        parsed = parse_weather_data(weather_json)
        display_weather(parsed)
    else:
        city_value.config(text="Error fetching data")
        temp_value.config(text="")
        feels_value.config(text="")
        humid_value.config(text="")
        desc_value.config(text="")
        icon_label.config(image="")

    # Forecast data
    forecast_json = get_forecast_data(location_input)
    if forecast_json:
        forecast_list = parse_forecast_data(forecast_json)
        display_forecast(forecast_list)
    else:
        # Clear forecast display if no data
        for widget in forecast_frame.winfo_children():
            widget.destroy()

def display_weather(parsed_data):
    """
    Update current weather display using parsed data.
    """
    city_str = parsed_data.get("city_name", "N/A")
    country_str = parsed_data.get("country", "N/A")
    temp_c = parsed_data.get("temp", "N/A")
    feels_c = parsed_data.get("feels_like", "N/A")
    humid_str = parsed_data.get("humidity", "N/A")
    desc_str = parsed_data.get("description", "N/A").capitalize()

    # Convert temperatures to Fahrenheit if possible
    temp_f = round((temp_c * 9 / 5) + 32, 1) if isinstance(temp_c, (int, float)) else "N/A"
    feels_f = round((feels_c * 9 / 5) + 32, 1) if isinstance(feels_c, (int, float)) else "N/A"

    city_value.config(text=f"{city_str}, {country_str}")
    temp_value.config(text=f"{temp_c}°C / {temp_f}°F")
    feels_value.config(text=f"{feels_c}°C / {feels_f}°F")
    humid_value.config(text=f"{humid_str}%")
    desc_value.config(text=desc_str)

    # Use helper function to get the icon
    icon_img = get_weather_icon(desc_str, size=(64, 64))
    if icon_img:
        icon_label.config(image=icon_img)
        icon_label.image = icon_img  # Keep a reference
    else:
        icon_label.config(image="")

def display_forecast(forecast_list):
    """
    Display forecast data as cards in the forecast_frame.
    Each card shows the date/time, a small icon, the temperature, and a brief description.
    """
    # Clear previous forecast cards
    for widget in forecast_frame.winfo_children():
        widget.destroy()

    # Create a card for each forecast item (displayed horizontally)
    for i, forecast in enumerate(forecast_list):
        card = ttk.Frame(forecast_frame, padding="10", style="Card.TFrame")
        card.grid(row=0, column=i, padx=10, pady=5)

        # Format the forecast time
        timestamp = forecast.get("timestamp")
        try:
            dt = datetime.fromtimestamp(timestamp)
            date_str = dt.strftime("%a %I:%M %p")
        except Exception:
            date_str = "N/A"
        date_label = ttk.Label(card, text=date_str, font=("Helvetica", 10, "bold"))
        date_label.pack(pady=(0, 5))

        # Forecast icon (smaller size)
        description = forecast.get("description", "N/A")
        icon_img = get_weather_icon(description, size=(32, 32))
        if icon_img:
            icon_label_forecast = ttk.Label(card, image=icon_img)
            icon_label_forecast.image = icon_img  # Keep a reference
            icon_label_forecast.pack(pady=(0, 5))

        # Temperature conversion
        temp_c = forecast.get("temp", "N/A")
        temp_f = round((temp_c * 9/5) + 32, 1) if isinstance(temp_c, (int, float)) else "N/A"
        temp_label = ttk.Label(card, text=f"{temp_c}°C / {temp_f}°F", font=("Helvetica", 10))
        temp_label.pack(pady=(0, 5))

        # Forecast description
        desc_label = ttk.Label(card, text=description.capitalize(), font=("Helvetica", 10))
        desc_label.pack()

# --- Main Window Setup ---
root = tb.Window(themename="superhero")
root.title("Python Weather")
root.geometry("700x700")
root.resizable(True, False)

# --- Layout ---

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Header
header_label = ttk.Label(main_frame, text="Python Weather", font=("Helvetica", 20, "bold"))
header_label.pack(pady=(0, 20))

# Input Frame (aligned using grid)
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=(0, 10), fill=tk.X)
input_frame.columnconfigure(1, weight=1)

city_label = ttk.Label(input_frame, text="Enter City or Zip:")
city_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

city_entry = ttk.Entry(input_frame, width=30)
city_entry.grid(row=0, column=1, sticky="ew")

get_weather_button = tb.Button(
    input_frame,
    text="Get Weather",
    command=fetch_weather,
    bootstyle="warning"  # Orange, rounded button from ttkbootstrap
)
get_weather_button.grid(row=0, column=2, padx=(10, 0))

# Current Weather Details Frame
details_frame = ttk.Frame(main_frame, padding="15")
details_frame.pack(fill=tk.X)

details_frame.columnconfigure(0, weight=0)
details_frame.columnconfigure(1, weight=1)
details_frame.columnconfigure(2, weight=0)

city_header = ttk.Label(details_frame, text="City:", font=("Helvetica", 12, "bold"))
city_header.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
city_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
city_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

temp_header = ttk.Label(details_frame, text="Temperature:", font=("Helvetica", 12, "bold"))
temp_header.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
temp_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
temp_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

feels_header = ttk.Label(details_frame, text="Feels like:", font=("Helvetica", 12, "bold"))
feels_header.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
feels_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
feels_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

humid_header = ttk.Label(details_frame, text="Humidity:", font=("Helvetica", 12, "bold"))
humid_header.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
humid_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
humid_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

desc_header = ttk.Label(details_frame, text="Description:", font=("Helvetica", 12, "bold"))
desc_header.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
desc_value = ttk.Label(details_frame, text="", font=("Helvetica", 12))
desc_value.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

icon_label = ttk.Label(details_frame)
icon_label.grid(row=0, column=2, rowspan=5, padx=(10, 0), pady=5, sticky="n")

# Forecast Frame (placed below current weather details)
forecast_frame = ttk.Frame(main_frame, padding="10")
forecast_frame.pack(fill=tk.X, pady=(10, 0))

root.mainloop()
