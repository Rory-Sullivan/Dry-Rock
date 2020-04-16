"""
Updates our local xml data files and the html report.
"""
import datetime as dt

from manage_places import get_places
from weather_data import WeatherData

NOW = dt.datetime.now()
print(f"Collecting weather data at {NOW}")

PLACES = get_places()

CURRENT_DATA = WeatherData(NOW, PLACES)

CURRENT_DATA.update_html_report()
