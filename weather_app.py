import requests
from datetime import datetime

API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/"
UNITS = {"metric": {"temp": "°C", "speed": "m/s"}, "imperial": {"temp": "°F", "speed": "mph"}}


def get_weather_data(query_type, params):
    try:
        response = requests.get(f"{BASE_URL}{query_type}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None


def get_coordinates(city, api_key):
    params = {"q": city, "appid": api_key}
    data = get_weather_data("weather", params)
    return (data["coord"]["lat"], data["coord"]["lon"]) if data else (None, None)


def get_current_weather(city, api_key, units="metric"):
    params = {"q": city, "appid": api_key, "units": units}
    return get_weather_data("weather", params)


def get_forecast(city, api_key, units="metric"):
    lat, lon = get_coordinates(city, api_key)
    if not lat or not lon:
        return None
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}
    return get_weather_data("forecast", params)


def get_wind_direction(degrees):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    return directions[round(degrees / 45) % 8]


def display_current_weather(data, units):
    if not data:
        return

    weather_main = data["weather"][0]["main"]
    emojis = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
        "Snow": "❄️", "Thunderstorm": "⛈️", "Mist": "🌫️"
    }

    print(f"\n{emojis.get(weather_main, '🌎')} Current Weather in {data['name']}, {data['sys']['country']}")
    print(f"🌡️ Temperature: {data['main']['temp']}{UNITS[units]['temp']}")
    print(f"🌡️ Feels like: {data['main']['feels_like']}{UNITS[units]['temp']}")
    print(f"💧 Humidity: {data['main']['humidity']}%")
    print(f"🎐 Wind: {data['wind']['speed']} {UNITS[units]['speed']} {get_wind_direction(data['wind']['deg'])}")
    print(f"☁️ Cloudiness: {data['clouds']['all']}%")
    print(f"🌄 Pressure: {data['main']['pressure']} hPa")
    print(f"👁️ Visibility: {data['visibility'] // 1000} km")
    print(f"📝 Conditions: {data['weather'][0]['description'].capitalize()}\n")


def display_forecast(data, units):
    if not data:
        return

    forecasts = {}
    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d")
        if date not in forecasts:
            forecasts[date] = {
                "temps": [],
                "weather": []
            }
        forecasts[date]["temps"].append(entry["main"]["temp"])
        forecasts[date]["weather"].append(entry["weather"][0]["main"])

    print("\n📅 5-Day Weather Forecast:")
    for date, values in list(forecasts.items())[:5]:
        avg_temp = sum(values["temps"]) / len(values["temps"])
        most_common_weather = max(set(values["weather"]), key=values["weather"].count)
        print(f"  {datetime.strptime(date, '%Y-%m-%d').strftime('%a %d %b')}: "
              f"{most_common_weather} | Avg Temp: {round(avg_temp, 1)}{UNITS[units]['temp']}")


def main():
    print("🌦️ Advanced Weather App 🌪️")
    units = input("Choose units (metric/imperial): ").lower() or "metric"

    while True:
        city = input("\nEnter city name (or 'q' to quit): ").strip()
        if city.lower() in ('q', 'quit'):
            break

        # Current weather
        current_data = get_current_weather(city, API_KEY, units)
        if current_data:
            display_current_weather(current_data, units)
        else:
            continue

        # 5-day forecast
        if input("Show 5-day forecast? (y/n): ").lower() == 'y':
            forecast_data = get_forecast(city, API_KEY, units)
            if forecast_data:
                display_forecast(forecast_data, units)

        # Additional options
        if input("Show raw data? (y/n): ").lower() == 'y':
            print("\n📄 Raw Data:")
            print(current_data)


if __name__ == "__main__":
    main()