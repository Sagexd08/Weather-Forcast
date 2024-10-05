import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Replace with your OpenWeatherMap API key
API_KEY = '6b5bed33fb773579ea27995d6b5fe3bc'

def get_weather_data(city, forecast=False):
    """Fetch weather data from OpenWeatherMap for a given city."""
    if forecast:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def display_current_weather(data):
    """Display the current weather data."""
    city_name = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "Unknown")
    temperature = data.get("main", {}).get("temp", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    wind_speed = data.get("wind", {}).get("speed", "N/A")
    description = data.get("weather", [{}])[0].get("description", "N/A")
    sunrise = datetime.utcfromtimestamp(data.get("sys", {}).get("sunrise", 0)).strftime('%H:%M:%S')
    sunset = datetime.utcfromtimestamp(data.get("sys", {}).get("sunset", 0)).strftime('%H:%M:%S')
    
    print(f"\nWeather in {city_name}, {country}:")
    print(f"Description: {description.capitalize()}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Sunrise: {sunrise} UTC")
    print(f"Sunset: {sunset} UTC")

def display_forecast_weather(data):
    """Display a 3-day weather forecast with a graph."""
    city_name = data.get("city", {}).get("name", "Unknown")
    country = data.get("city", {}).get("country", "Unknown")
    
    print(f"\n3-Day Weather Forecast for {city_name}, {country}:")
    
    dates = []
    temps = []
    
    for forecast in data.get("list", [])[:24:8]:  # 3 days forecast (API provides every 3 hours)
        date = datetime.utcfromtimestamp(forecast.get("dt", 0)).strftime('%Y-%m-%d %H:%M:%S')
        temperature = forecast.get("main", {}).get("temp", "N/A")
        description = forecast.get("weather", [{}])[0].get("description", "N/A")
        
        dates.append(date)
        temps.append(temperature)
        
        print(f"Date: {date}")
        print(f"Temperature: {temperature}°C")
        print(f"Weather: {description.capitalize()}")
        print("-" * 40)
    
    if dates and temps:
        # Plot temperature trend
        plt.figure(figsize=(10, 6))
        plt.plot(dates, temps, marker="o", color="b")
        plt.xticks(rotation=45)
        plt.xlabel("Date and Time")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Temperature Trend for {city_name}")
        plt.tight_layout()
        plt.show()
    else:
        print("Not enough data to display the temperature trend.")

def run_weather_app():
    """Main function to run the weather app."""
    while True:
        print("\n==== Weather Forecasting App ====")
        print("1. Current Weather")
        print("2. 3-Day Forecast")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "3":
            print("Exiting the app. Goodbye!")
            break
        
        if choice not in ["1", "2"]:
            print("Invalid choice. Please try again.")
            continue
        
        city = input("\nEnter a city name: ").strip()
        if not city:
            print("Please enter a valid city name.")
            continue
        
        if choice == "1":
            # Fetch and display current weather
            weather_data = get_weather_data(city)
            if weather_data:
                display_current_weather(weather_data)
        
        elif choice == "2":
            # Fetch and display 3-day forecast
            forecast_data = get_weather_data(city, forecast=True)
            if forecast_data:
                display_forecast_weather(forecast_data)

if __name__ == "__main__":
    run_weather_app()
