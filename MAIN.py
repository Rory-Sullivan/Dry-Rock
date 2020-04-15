"""
Updates our local xml data files and the html report.
"""
import datetime as dt

from general_classes import Place
from manage_places import get_places
from weather_data import WeatherData

# Get a time for this run.
NOW = dt.datetime.now()
print(f"Collecting weather data at {NOW}")

# Get places we are going to check.
if __name__ == "__main__":
    PLACES = get_places()
# For testing purposes we will just use Dublin.
else:
    PLACES = [
        Place(
            "Dublin",
            "Ireland/Leinster/Dublin",
            "https://www.yr.no/en/forecast/daily-table/2-2964574",
        )
    ]


CURRENT_DATA = WeatherData(NOW, PLACES)


CURRENT_DATA.update_html_report()
