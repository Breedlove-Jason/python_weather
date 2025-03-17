import cache
import weather_api
import gui
import cairosvg

def main():

    user_city = input("Enter the city name: ")

    # get current weather data
    data = weather_api.get_weather_data(user_city)
    check_for_data = cache.read_cached_weather_data("cache.txt")
    parsed_data = weather_api.parse_weather_data(data)
    if check_for_data == parsed_data:
        print("Data already exists in cache")
    else:
        print("Data does not exist in cache")
        cache.cache_weather_data(data, "cache.txt")
    for items in parsed_data:
        print(items)

    # get 5-day forecast data
    forecast_data = weather_api.get_forecast_data(user_city)
    parsed_forecast_data = weather_api.parse_forecast_data(forecast_data)
    cached_data = cache.read_cached_weather_data("forecast_cache.txt", expiry_seconds=3600)
    if cached_data:
        print("Using cached forecast data.")
        # Use cached_data
    else:
        print("Fetching fresh forecast data.")
        cache.cache_weather_data(parsed_forecast_data, "forecast_cache.txt")
    for items in parsed_forecast_data:
        print("Forecast", items)

    gui.display_weather(parsed_data)

if __name__ == "__main__":
    main()