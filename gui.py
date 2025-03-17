from tkinter import Label, Tk, Entry, Button
from weather_api import get_weather_data, parse_weather_data
from PIL import ImageTk, Image  # For image handling (needs pillow)
from utils import load_svg_as_photoimage
root = Tk()
root.title("Python Weather App")

# --- Weather Icons ---
icon_paths = {
    "clear": "./icons/sun-sharp-solid.svg",
    "snow": "./icons/snowflake-sharp-solid.svg",
    "rain": "./icons/umbrella-sharp-solid.svg",
    "cloud": "./icons/cloud-sharp-solid.svg",
    "thunder": "./icons/bolt-sharp-solid.svg"
}
# --- Widgets ---
city_entry = Entry(root)
city_entry.pack()

get_weather_button = Button(root, text="Get Weather", command=lambda: fetch_weather())
get_weather_button.pack()

result_label = Label(root, text="")
result_label.pack()

# Icon placeholder
icon_label = Label(root)
icon_label.pack()

#  --- Functions ---

def fetch_weather():
    city = city_entry.get()
    weather_json = get_weather_data(city)
    if weather_json:
        parsed = parse_weather_data(weather_json)
        display_weather(parsed)
    else:
        result_label.config(text="Error fetching weather.")


def display_weather(parsed_data):
    result_label.config(
        text=f"City: {parsed_data['city']}, {parsed_data['country']}\n"
        f"Temperature: {parsed_data['temp']}°C\n"
        f"Feels like: {parsed_data['feels_like']}°C\n"
        f"Humidity: {parsed_data['humidity']}%\n"
        f"Description: {parsed_data['description']}\n")

    # Narrowing of results to specific items
    desc = parsed_data['description']
    icon_key = None

    if "clear" in desc:
        icon_key = "clear"
    elif "cloud" in desc:
        icon_key = "cloud"
    elif "rain" in desc:
        icon_key = "rain"
    elif "snow" in desc:
        icon_key = "snow"
    elif "thunder" in desc:
        icon_key = "thunder"

    if icon_key:
        icon_img = load_svg_as_photoimage(icon_paths[icon_key], size=(64, 64))
        icon_label.config(image=icon_img)
        icon_label.image = icon_img
    else:
        icon_label.config(image="")

root.mainloop()



