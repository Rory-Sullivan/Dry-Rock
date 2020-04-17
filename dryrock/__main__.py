"""
Updates our local xml data files and the html report.
"""
import os
import datetime as dt

from helpers.manage_places import get_places
from helpers.weather_data import WeatherData

if not os.path.isdir("./data/output/"):
    os.mkdir("./data/output/")

NOW = dt.datetime.now()
print(f"Collecting weather data at {NOW}")

PLACES = get_places()

CURRENT_DATA = WeatherData(NOW, PLACES)

CURRENT_DATA.update_html_report()
print("Done")
