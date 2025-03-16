
import weather_api
from weather_api import parse_weather_data


def main():


    user_city = input("Enter the city name: ")
    data = weather_api.get_weather_data(user_city)
    parsed_data = weather_api.parse_weather_data(data)
    for items in parsed_data:
        print(items)
if __name__ == "__main__":
    main()