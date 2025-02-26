import requests

API_KEY = "YOUR_API_KEY"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city, api_key):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found.")
        else:
            print(f"Error: Received status code {response.status_code}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None


def display_weather(data):
    if not data:
        return

    # Extract weather data
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather_desc = data["weather"][0]["description"].capitalize()
    weather_main = data["weather"][0]["main"]

    # Add emojis based on weather condition
    emoji = "🌫️"  # Default emoji
    if weather_main == "Clear":
        emoji = "☀️"
    elif weather_main == "Clouds":
        emoji = "☁️"
    elif weather_main == "Rain":
        emoji = "🌧️"
    elif weather_main == "Snow":
        emoji = "❄️"

    # Display formatted weather info
    print(f"\nWeather in {city}, {country} {emoji}")
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Conditions: {weather_desc}\n")


def main():
    print("Weather App - Get Current Weather Conditions")
    while True:
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        if city.lower() == "quit":
            print("Exiting the program. Goodbye!")
            break

        weather_data = get_weather(city, API_KEY)
        if weather_data:
            display_weather(weather_data)


if __name__ == "__main__":
    main()