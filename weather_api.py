import dotenv
import os
import requests

# load env file and get api key
dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

user_city = input("Enter the city name: ")


def get_weather_data(city_name):
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print(f"City '{city_name}' not found. Please check spelling.\n")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return None


def get_forecast_data(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 5,
    }
    try:
        forecast_data = requests.get(FORECAST_URL, params=params).json()
        forecast_data.raise_for_status()
        return forecast_data
    except requests.exceptions.HTTPError:
        print(f"City '{city_name}' not found. Please check spelling.\n")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return None


def parse_weather_data(api_data):
    city_name = data.get("name")
    country = data.get("sys", {}).get("country")
    temp = data.get("main", {}).get("temp")
    feels_like = data.get("main", {}).get("feels_like")
    humidity = data.get("main", {}).get("humidity")
    description = data.get("weather", [{}])[0].get("description")
    wind_speed = data.get("wind", {}).get("speed")
    wind_deg = data.get("wind", {}).get("deg")
    timestamp = data.get("dt")
    sunrise = data.get("sys", {}).get("sunrise")
    sunset = data.get("sys", {}).get("sunset")
