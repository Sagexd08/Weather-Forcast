import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# OpenWeatherMap API settings
API_KEY = "6b5bed33fb773579ea27995d6b5fe3bc"
BASE_URL = "http://api.openweathermap.org/data/2.5"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        # City Entry
        ttk.Label(self.root, text="City:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_city = ttk.Entry(self.root, width=30)
        self.entry_city.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        # Unit Selection
        self.var_unit = tk.StringVar(value="metric")
        ttk.Label(self.root, text="Unit:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(self.root, text="Celsius", variable=self.var_unit, value="metric").grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.root, text="Fahrenheit", variable=self.var_unit, value="imperial").grid(row=1, column=2, padx=5, pady=5)

        # Buttons
        ttk.Button(self.root, text="Current Weather", command=self.get_current_weather).grid(row=2, column=0, padx=5, pady=5, columnspan=3, sticky='ew')
        ttk.Button(self.root, text="3-Day Forecast", command=self.get_forecast).grid(row=3, column=0, padx=5, pady=5, columnspan=3, sticky='ew')

        # Results Display
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=4, column=0, padx=5, pady=5, columnspan=3)

        # Graph Display
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=5, column=0, padx=5, pady=5, columnspan=3)

        # Image Display
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=6, column=0, padx=5, pady=5, columnspan=3)

    def get_weather_data(self, city, unit="metric", forecast=False):
        params = {
            "q": city,
            "units": unit,
            "appid": API_KEY
        }
        endpoint = "forecast" if forecast else "weather"
        url = f"{BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
            return None

    def get_current_weather(self):
        city = self.entry_city.get()
        if not city:
            messagebox.showerror("Error", "Please enter a valid city name.")
            return
        
        data = self.get_weather_data(city, self.var_unit.get())
        if data:
            self.display_current_weather(data)

    def get_forecast(self):
        city = self.entry_city.get()
        if not city:
            messagebox.showerror("Error", "Please enter a valid city name.")
            return
        
        data = self.get_weather_data(city, self.var_unit.get(), forecast=True)
        if data:
            self.display_forecast(data)

    def display_current_weather(self, data):
        temp_unit = "°C" if self.var_unit.get() == "metric" else "°F"
        weather_info = f"""
Current Weather for {data['name']}, {data['sys']['country']}:
Temperature: {data['main']['temp']}{temp_unit}
Feels Like: {data['main']['feels_like']}{temp_unit}
Humidity: {data['main']['humidity']}%
Weather: {data['weather'][0]['description'].capitalize()}
Wind Speed: {data['wind']['speed']} m/s
        """
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, weather_info)

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        response = requests.get(icon_url)
        image_data = response.content
        image = tk.PhotoImage(data=image_data)
        self.image_label.config(image=image)
        self.image_label.image = image

    def display_forecast(self, data):
        temp_unit = "°C" if self.var_unit.get() == "metric" else "°F"
        forecast_info = f"3-Day Forecast for {data['city']['name']}, {data['city']['country']}:\n\n"
        
        dates = []
        temps = []
        for forecast in data['list'][:8:2]:  # Every 24 hours for 3 days
            date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
            dates.append(date)
            temps.append(forecast['main']['temp'])
            forecast_info += f"""
Date: {date}
Temperature: {forecast['main']['temp']}{temp_unit}
Feels Like: {forecast['main']['feels_like']}{temp_unit}
Humidity: {forecast['main']['humidity']}%
Weather: {forecast['weather'][0]['description'].capitalize()}
Wind Speed: {forecast['wind']['speed']} m/s
            
"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, forecast_info)

        # Display graph
        self.ax.clear()
        self.ax.plot(dates, temps)
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel(f'Temperature ({temp_unit})')
        self.ax.set_title('3-Day Forecast')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
