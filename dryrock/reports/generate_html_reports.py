from copy import deepcopy
import pathlib
import datetime as dt

import jinja2 as jinja

from dryrock.forecasts.combined import WeatherData
from dryrock.forecasts.yr import YrData


def get_context(data: WeatherData):
    today = dt.date.today()
    days = [today + dt.timedelta(days=i) for i in range(7)]

    places = []
    for place in data.places:
        relevant_forecast = data.yr_data_for_places[place.name].long_range_forecast

        forecasts = []
        for day in days:
            forecast = {
                "day": day,
                "intervals": relevant_forecast.get_relevant_intervals(day),
            }

            total_rain = 0
            temperatures = []
            wind_speeds = []
            for interval in forecast["intervals"]:
                total_rain += interval.variables_dict["precipitation"].value
                temperatures.append(interval.variables_dict["temperature"])
                wind_speeds.append(interval.variables_dict["wind"])

            forecast["total_rain"] = {
                "value": total_rain,
                "unit": forecast["intervals"][0].variables_dict["precipitation"].unit,
            }
            forecast["max_temp"] = max(temperatures, key=lambda var: var.value)
            forecast["min_temp"] = min(temperatures, key=lambda var: var.value)
            forecast["max_wind_speed"] = max(wind_speeds, key=lambda var: var.value)

            forecasts.append(forecast)

        places.append(
            {
                "name": place.name,
                "climbing_area": place.climbing_area,
                "yr_link": place.yr_link,
                "cite_yr": YrData.cite_text,
                "updated_at": relevant_forecast.updated_at,
                "sunrise_time": relevant_forecast.sunrise,
                "sunset_time": relevant_forecast.sunset,
                "forecasts": forecasts,
            }
        )

    context = {
        "days": days,
        "places": places,
    }
    return context


def update_html_report(data: WeatherData, output_path: pathlib.Path):
    """Updates index.html"""

    reports_path = output_path.joinpath("webpages/")

    if not reports_path.exists():
        reports_path.mkdir(parents=True)

    file_path = reports_path.joinpath(f"index.html")

    context = get_context(data)

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
