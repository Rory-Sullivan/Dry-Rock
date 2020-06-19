"""
Updates our local xml data files and the html report.
"""
import datetime as dt
import os

from dryrock.config import OUTPUT_PATH
from dryrock.forecasts.combined import WeatherData
from dryrock.places import get_places
from dryrock.reports.generate_html_reports import update_html_report
from dryrock.copy_reports import copy_index

if __name__ == "__main__":

    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    NOW = dt.datetime.now()
    print(f"Collecting weather data at {NOW}")

    PLACES = get_places()

    CURRENT_DATA = WeatherData(NOW, PLACES, OUTPUT_PATH)

    update_html_report(CURRENT_DATA, OUTPUT_PATH)
    copy_index()

    print("Done")
