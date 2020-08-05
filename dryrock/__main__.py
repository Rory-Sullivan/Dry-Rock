"""
Updates our local xml data files and the html report.
"""
import datetime as dt
import pathlib
from typing import List

from metno_locationforecast import Forecast

from .config import OUTPUT_PATH, PLACES_FILE
from .copy_reports import copy_index
from .places import get_places
from .reports.generate_html_reports import update_html_report

if __name__ == "__main__":

    output_path = pathlib.Path(OUTPUT_PATH)

    if not output_path.is_dir():
        output_path.mkdir(parents=True)

    now = dt.datetime.now()
    print(f"Collecting weather data at {now}")

    places = get_places(PLACES_FILE)

    forecasts: List[Forecast] = []
    for place in places:
        forecasts.append(Forecast(place))

    for forecast in forecasts:
        forecast.update()

        for interval in forecast.data.intervals:
            for variable in interval.variables.values():
                if variable.name == "wind_speed":
                    variable.convert_to("km/h")

    update_html_report(forecasts, OUTPUT_PATH)
    copy_index()

    print("Done")
