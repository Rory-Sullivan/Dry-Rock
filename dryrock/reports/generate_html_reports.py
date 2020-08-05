import datetime as dt
import pathlib
from typing import List

import jinja2 as jinja
from metno_locationforecast import Forecast
from metno_locationforecast.data_containers import Variable


def convert_deg_to_str(wind_variable: Variable):
    assert wind_variable.name == "wind_from_direction"
    assert wind_variable.units == "degrees"

    value = wind_variable.value
    if (337.5 <= value < 360) or (0 <= value < 22.5):
        direction_name = "North"
    elif 22.5 <= value < 67.5:
        direction_name = "Northeast"
    elif 67.5 <= value < 112.5:
        direction_name = "East"
    elif 112.5 <= value < 157.5:
        direction_name = "Southeast"
    elif 157.5 <= value < 202.5:
        direction_name = "South"
    elif 202.5 <= value < 247.5:
        direction_name = "Southwest"
    elif 247.5 <= value < 292.5:
        direction_name = "West"
    elif 292.5 <= value < 337.5:
        direction_name = "Northwest"
    else:
        raise ValueError("convert_deg_to_str has failed")
    return Variable("wind_from_direction", direction_name, "str")  # type: ignore


def get_context(forecasts: List[Forecast]):
    today = dt.date.today()

    days = [today + dt.timedelta(days=i) for i in range(7)]

    places = []
    context_forecasts = {}
    for forecast in forecasts:
        places.append(forecast.place)

        forecasts_for_place = []
        for day in days:
            relevant_intervals = forecast.data.intervals_for(day)

            current_total_rain = Variable("precipitation_amount", 0.0, "mm")
            current_max_temp = Variable("air_temperature", float("-inf"), "celsius")
            current_min_temp = Variable("air_temperature", float("inf"), "celsius")
            current_max_wind_speed = Variable("wind_speed", float("-inf"), "km/h")
            current_max_wind_speed_direction = Variable("wind_from_direction", 0.0, "degrees")
            context_intervals = []
            for interval in relevant_intervals:
                current_total_rain += interval.variables["precipitation_amount"]

                if current_max_temp.value < interval.variables["air_temperature"].value:
                    current_max_temp = interval.variables["air_temperature"]
                if current_min_temp.value > interval.variables["air_temperature"].value:
                    current_min_temp = interval.variables["air_temperature"]
                if current_max_wind_speed.value < interval.variables["wind_speed"].value:
                    current_max_wind_speed = interval.variables["wind_speed"]
                    current_max_wind_speed_direction = interval.variables["wind_from_direction"]

                context_interval = {
                    "start_time": interval.start_time,
                    "end_time": interval.end_time,
                    "rain": interval.variables["precipitation_amount"],
                }
                context_intervals.append(context_interval)

            current_max_wind_speed_direction = convert_deg_to_str(current_max_wind_speed_direction)

            forecast_for_day = {
                "day": day,
                "total_rain": current_total_rain,
                "max_temp": current_max_temp,
                "min_temp": current_min_temp,
                "max_wind_speed": current_max_wind_speed,
                "max_wind_speed_direction": current_max_wind_speed_direction,
                "intervals": context_intervals,
            }

            forecasts_for_place.append(forecast_for_day)

        context_forecasts[forecast.place.name] = forecasts_for_place

    context = {
        "days": days,
        "places": places,
        "forecasts": context_forecasts,
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
