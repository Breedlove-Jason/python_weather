import json
import time

def cache_weather_data(data, filename="cache.txt"):
    cache = {
        "timestamp": int(time.time()),
        "data": data
    }
    with open(filename, "w") as f:
        json.dump(cache, f)

def read_cached_weather_data(filename="cache.txt", expiry_seconds=3600):
    try:
        with open(filename, "r") as f:
            cache = json.load(f)
            cache_time = cache.get("timestamp", 0)
            if (int(time.time()) - cache_time) > expiry_seconds:
                print("Cache expired.")
                return None
            return cache["data"]
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Cache file {filename} not usable.")
        return None
