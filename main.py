
import weather_api
from weather_api import parse_weather_data


def main():



    user_city = input("Enter the city name: ")

    # get current weather data
    data = weather_api.get_weather_data(user_city)
    parsed_data = weather_api.parse_weather_data(data)
    for items in parsed_data:
        print(items)

    # get 5-day forecast data
    forecast_data = weather_api.get_forecast_data(user_city)
    parsed_forecast_data = weather_api.parse_forecast_data(forecast_data)
    for items in parsed_forecast_data:
        print("Forecast", items)

if __name__ == "__main__":
    main()