import dotenv
import os
import requests

# load env file and get api key
dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"


def get_weather_data(location):
    if location.isdigit():
        # Treat the input as a US zip code
        params = {"zip": f"{location},us", "appid": API_KEY, "units": "metric"}
    else:
        # Otherwise, treat it as a city name
        params = {"q": location, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print(f"Location '{location}' not found. Please check spelling or ZIP.\n")
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
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()
        forecast_data = response.json()
        return forecast_data
    except requests.exceptions.HTTPError:
        print(f"City '{city_name}' not found. Please check spelling.\n")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return None


def parse_weather_data(api_data):
    print(type(api_data))
    data = {
        "city_name": api_data.get("name"),
        "country": api_data.get("sys", {}).get("country"),
        "temp": api_data.get("main", {}).get("temp"),
        "feels_like": api_data.get("main", {}).get("feels_like"),
        "humidity": api_data.get("main", {}).get("humidity"),
        "description": api_data.get("weather", [{}])[0].get("description"),
        "wind_speed": api_data.get("wind", {}).get("speed"),
        "wind_deg": api_data.get("wind", {}).get("deg"),
        "timestamp": api_data.get("dt"),
        "sunrise": api_data.get("sys", {}).get("sunrise"),
        "sunset": api_data.get("sys", {}).get("sunset"),
    }

    return data


def parse_forecast_data(forecast_data):
    forecast_list = []
    for forecast in forecast_data.get("list", []):
        forecast_list.append(
            {
                "timestamp": forecast.get("dt"),
                "temp": forecast.get("main", {}).get("temp"),
                "feels_like": forecast.get("main", {}).get("feels_like"),
                "humidity": forecast.get("main", {}).get("humidity"),
                "description": forecast.get("weather", [{}])[0].get("description"),
            }
        )
    return forecast_list
