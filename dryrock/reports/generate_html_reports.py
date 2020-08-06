import datetime as dt
import pathlib
from typing import List

import jinja2 as jinja
from metno_locationforecast import Forecast

from .helper_functions import (
    cardinal_name_of,
    max_temp_of,
    max_wind_speed_of,
    min_temp_of,
    sum_rain,
)


def get_context(forecasts: List[Forecast]):
    today = dt.date.today()
    morning_times = [dt.time(6), dt.time(11, 59)]
    afternoon_times = [dt.time(12), dt.time(17, 59)]
    evening_times = [dt.time(18), dt.time(23, 59)]

    days = [today + dt.timedelta(days=i) for i in range(7)]

    places = []
    context_forecasts = {}
    forecast_updated_at = {}
    for forecast in forecasts:
        places.append(forecast.place)

        forecasts_for_place = {}
        for day in days:
            days_intervals = forecast.data.intervals_for(day)
            days_rain = sum_rain(days_intervals)
            days_max_temp = max_temp_of(days_intervals)
            days_min_temp = min_temp_of(days_intervals)
            days_max_wind_speed, days_max_wind_speed_direction = max_wind_speed_of(days_intervals)
            days_max_wind_speed.convert_to("km/h")

            morning = [dt.datetime.combine(day, time) for time in morning_times]
            morning_intervals = forecast.data.intervals_between(morning[0], morning[1])
            morning_rain = sum_rain(morning_intervals)

            afternoon = [dt.datetime.combine(day, time) for time in afternoon_times]
            afternoon_intervals = forecast.data.intervals_between(afternoon[0], afternoon[1])
            afternoon_rain = sum_rain(afternoon_intervals)

            evening = [dt.datetime.combine(day, time) for time in evening_times]
            evening_intervals = forecast.data.intervals_between(evening[0], evening[1])
            evening_rain = sum_rain(evening_intervals)

            forecast_for_day = {
                "total_rain": days_rain,
                "morning_rain": morning_rain,
                "afternoon_rain": afternoon_rain,
                "evening_rain": evening_rain,
                "max_temp": days_max_temp,
                "min_temp": days_min_temp,
                "max_wind_speed": days_max_wind_speed,
                "max_wind_speed_direction": cardinal_name_of(days_max_wind_speed_direction),
                "intervals": days_intervals,
            }

            forecasts_for_place[day] = forecast_for_day

        context_forecasts[forecast.place.name] = forecasts_for_place
        forecast_updated_at[forecast.place.name] = forecast.data.updated_at

    context = {
        "days": days,
        "places": places,
        "forecasts": context_forecasts,
        "updated_at": forecast_updated_at,
    }
    return context


def update_html_report(forecasts: List[Forecast], output_path: str):
    """Updates index.html"""

    reports_path = pathlib.Path(output_path).joinpath("webpages/")

    if not reports_path.is_dir():
        reports_path.mkdir(parents=True)

    file_path = reports_path.joinpath("index.html")

    context = get_context(forecasts)

    env = jinja.Environment(
        loader=jinja.FileSystemLoader("./dryrock/reports/templates"),
        autoescape=jinja.select_autoescape(),  # Enable auto escaping.
        trim_blocks=True,  # Stops blocks from rendering a blank line.
        lstrip_blocks=True,  # Strips whitespace from in front of a block.
    )

    template = env.get_template("base.html.j2")

    output = template.render(context)

    with open(file_path, "w") as file:
        file.write(output)
