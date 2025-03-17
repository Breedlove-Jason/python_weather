import json


def cache_weather_data(data, filename="cache.txt"):
    with open(filename, "w") as f:
        json.dump(data, f)

