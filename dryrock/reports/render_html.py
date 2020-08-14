import datetime as dt
import pathlib
from typing import Dict, List, Optional

import jinja2 as jinja
from metno_locationforecast import Forecast

from .helper_functions import (
    cardinal_name_of,
    change_units,
    max_temp_of,
    max_wind_speed_of,
    min_temp_of,
    sum_rain,
)


def get_context(forecasts: List[Forecast]):
    """Returns a context variable for passing into our template."""

    today = dt.date.today()
    morning_times = [dt.time(6), dt.time(11, 59)]
    afternoon_times = [dt.time(12), dt.time(17, 59)]
    evening_times = [dt.time(18), dt.time(23, 59)]

    days = [today + dt.timedelta(days=i) for i in range(7)]

    change_units(forecasts)

    places = []
    context_forecasts = {}
    forecast_updated_at = {}
    for forecast in forecasts:
        places.append(forecast.place)

        forecasts_for_place: Dict[dt.date, Optional[object]] = {}
        for day in days:
            days_intervals = forecast.data.intervals_for(day)

            if len(days_intervals) > 0:
                days_rain = sum_rain(days_intervals)
                days_max_temp = max_temp_of(days_intervals)
                days_min_temp = min_temp_of(days_intervals)
                days_max_wind_speed, days_max_wind_speed_direction = max_wind_speed_of(
                    days_intervals
                )
                days_max_wind_speed.convert_to("km/h")

                morning = [dt.datetime.combine(day, time) for time in morning_times]
                morning_intervals = forecast.data.intervals_between(morning[0], morning[1])
                morning_rain = sum_rain(morning_intervals) if len(morning_intervals) > 0 else None

                afternoon = [dt.datetime.combine(day, time) for time in afternoon_times]
                afternoon_intervals = forecast.data.intervals_between(afternoon[0], afternoon[1])
                afternoon_rain = (
                    sum_rain(afternoon_intervals) if len(afternoon_intervals) > 0 else None
                )

                evening = [dt.datetime.combine(day, time) for time in evening_times]
                evening_intervals = forecast.data.intervals_between(evening[0], evening[1])
                evening_rain = sum_rain(evening_intervals) if len(evening_intervals) > 0 else None

                intervals = []
                for day_interval in days_intervals:
                    interval = {
                        "start_time": day_interval.start_time,
                        "end_time": day_interval.end_time,
                        "rain": day_interval.variables["precipitation_amount"],
                        "temp": day_interval.variables["air_temperature"],
                        "wind_speed": day_interval.variables["wind_speed"],
                        "wind_from_direction": cardinal_name_of(
                            day_interval.variables["wind_from_direction"]
                        ),
                    }
                    intervals.append(interval)

                forecast_for_day = {
                    "total_rain": days_rain,
                    "max_temp": days_max_temp,
                    "min_temp": days_min_temp,
                    "max_wind_speed": days_max_wind_speed,
                    "max_wind_speed_direction": cardinal_name_of(days_max_wind_speed_direction),
                    "morning_rain": morning_rain,
                    "afternoon_rain": afternoon_rain,
                    "evening_rain": evening_rain,
                    "intervals": intervals,
                }

                forecasts_for_place[day] = forecast_for_day

            else:
                forecasts_for_place[day] = None

        context_forecasts[forecast.place.name] = forecasts_for_place
        forecast_updated_at[forecast.place.name] = forecast.data.updated_at

    context = {
        "days": days,
        "places": places,
        "forecasts": context_forecasts,
        "updated_at": forecast_updated_at,
    }
    return context


def render_html_pages(forecasts: List[Forecast]):
    """Updates index.html"""

    webpages_path = pathlib.Path("./pages/")
    if not webpages_path.is_dir():
        webpages_path.mkdir(parents=True)

    env = jinja.Environment(
        loader=jinja.FileSystemLoader("./dryrock/reports/templates"),
        autoescape=jinja.select_autoescape(),  # Enable auto escaping.
        trim_blocks=True,  # Stops blocks from rendering a blank line.
        lstrip_blocks=True,  # Strips whitespace from in front of a block.
    )

    index_file_path = webpages_path.joinpath("index.html")
    about_file_path = webpages_path.joinpath("about.html")
    news_file_path = webpages_path.joinpath("news.html")

    index_template = env.get_template("index.html.j2")
    about_template = env.get_template("about.html.j2")
    news_template = env.get_template("news.html.j2")

    index_context = get_context(forecasts)

    # Note the encoding method, this returns a bytes string so these need to be written to files in
    # bytes mode
    index_output = index_template.render(index_context).encode("utf8")
    about_output = about_template.render().encode("utf8")
    news_output = news_template.render().encode("utf8")

    with open(index_file_path, "wb") as file:
        file.write(index_output)

    with open(about_file_path, "wb") as file:
        file.write(about_output)

    with open(news_file_path, "wb") as file:
        file.write(news_output)
