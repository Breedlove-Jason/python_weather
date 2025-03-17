from tkinter import Label, Tk
from weather_api import get_weather_data, parse_weather_data
from PIL import ImageTk, Image  # For image handling (needs pillow)
from utils import load_svg_as_photoimage
root = Tk()
root.title("Python Weather App")
result_label = Label(root, text="")

sun_sharp_svg = "./icons/sun-sharp-solid.svg"
sun_icon = load_svg_as_photoimage(sun_sharp_svg, size=(64, 64))
sun_icon_label = Label(root, image=sun_icon)
sun_icon_label.pack()

snow_sharp_svg = "./icons/snowflake-sharp-solid.svg"
snow_icon = load_svg_as_photoimage(snow_sharp_svg, size=(64, 64))
snow_icon_label = Label(root, image=snow_icon)
snow_icon_label.pack()

umbrella_sharp_svg = "./icons/umbrella-sharp-solid.svg"
umbrella_icon = load_svg_as_photoimage(umbrella_sharp_svg, size=(64, 64))
umbrella_icon_label = Label(root, image=umbrella_icon)
umbrella_icon_label.pack()

cloud_sharp_svg = "./icons/cloud-sharp-solid.svg"
cloud_icon = load_svg_as_photoimage(cloud_sharp_svg, size=(64, 64))
cloud_icon_label = Label(root, image=cloud_icon)
cloud_icon_label.pack()

bolt_sharp_svg = "./icons/bolt-sharp-solid.svg"
bolt_icon = load_svg_as_photoimage(bolt_sharp_svg, size=(64, 64))
bolt_icon_label = Label(root, image=bolt_icon)
bolt_icon_label.pack()

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
        f"Description: {parsed_data['description']}\n"
    )


root.mainloop()
