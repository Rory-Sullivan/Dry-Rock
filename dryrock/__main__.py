"""
Updates our local xml data files and the html report.
"""
import os
import datetime as dt

from dryrock.places.manage_places import get_places
from dryrock.forecasts.combined import WeatherData
from dryrock.config import OUTPUT_PATH

if __name__ == "__main__":

    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    NOW = dt.datetime.now()
    print(f"Collecting weather data at {NOW}")

    PLACES = get_places()

    CURRENT_DATA = WeatherData(NOW, PLACES, OUTPUT_PATH)

    CURRENT_DATA.update_html_report()
    print("Done")
