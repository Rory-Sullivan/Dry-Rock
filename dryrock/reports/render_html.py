import copy
import datetime as dt
import pathlib
from typing import Any, Dict, List, Optional

import jinja2 as jinja
from metno_locationforecast import Forecast, Place
from places import Area

from .helper_functions import (
    cardinal_name_of,
    change_units,
    max_temp_of,
    max_wind_speed_of,
    min_temp_of,
    sanitize_name,
    sum_rain,
)


def get_navbar_context(areas: List[Area]) -> Dict[str, Any]:
    nav_links: List[Dict[str, Any]] = []
    for area in areas:
        nav_links.append(
            {
                "name": area.name,
                "href": f"/pages/{sanitize_name(area.name)}.html",
                "is_active": False,
            }
        )
    nav_links.append({"name": "About", "href": "/pages/about.html", "is_active": False})
    nav_links.append({"name": "News", "href": "/pages/news.html", "is_active": False})
    return {"nav_links": nav_links}


def get_area_forecast_context(
    places: List[Place],
    place_forecasts: List[Forecast],
    days: List[dt.date],
    morning_times: List[dt.time],
    afternoon_times: List[dt.time],
    evening_times: List[dt.time],
) -> Dict[str, Any]:
    if len(places) != len(place_forecasts):
        raise ValueError("Number of places must match the number of place forecasts")

    context_forecasts = {}
    forecast_updated_at = {}
    for forecast in place_forecasts:
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

                intervals: List[Dict[str, Any]] = []
                for day_interval in days_intervals:
                    interval: Dict[str, Any] = {
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

                forecast_for_day: Dict[str, Any] = {
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

    context: Dict[str, Any] = {
        "days": days,
        "places": places,
        "forecasts": context_forecasts,
        "updated_at": forecast_updated_at,
    }
    return context


def get_forecast_page_contexts(
    areas: List[Area], area_forecasts: List[List[Forecast]]
) -> List[Dict[str, Any]]:
    """Returns a list of contexts one each per area for passing into the forecast page template."""

    if len(areas) != len(area_forecasts):
        raise ValueError("Number of areas must match the number of area forecasts")

    nav_bar_context = get_navbar_context(areas)

    for place_forecasts in area_forecasts:
        change_units(place_forecasts)

    today = dt.date.today()
    morning_times = [dt.time(6), dt.time(11, 59)]
    afternoon_times = [dt.time(12), dt.time(17, 59)]
    evening_times = [dt.time(18), dt.time(23, 59)]
    days = [today + dt.timedelta(days=i) for i in range(7)]

    forecast_page_contexts: List[Dict[str, Any]] = []
    for i, area in enumerate(areas):
        place_forecasts = area_forecasts[i]

        context = get_area_forecast_context(
            area.places, place_forecasts, days, morning_times, afternoon_times, evening_times
        )
        context["nav_links"] = copy.deepcopy(nav_bar_context["nav_links"])
        context["nav_links"][i]["is_active"] = True
        forecast_page_contexts.append(context)

    return forecast_page_contexts


def get_about_page_context(areas: List[Area]) -> Dict[str, Any]:
    context = get_navbar_context(areas)
    context["nav_links"][len(areas)]["is_active"] = True
    return context


def get_news_page_context(areas: List[Area]) -> Dict[str, Any]:
    context = get_navbar_context(areas)
    context["nav_links"][len(areas) + 1]["is_active"] = True
    return context


def render_html_pages(areas: List[Area], area_forecasts: List[List[Forecast]]):
    """Renders all HTML pages, saving them to the pages folder"""

    webpages_path = pathlib.Path("./pages/")
    if not webpages_path.is_dir():
        webpages_path.mkdir(parents=True)

    env = jinja.Environment(
        loader=jinja.FileSystemLoader("./dryrock/reports/templates"),
        autoescape=jinja.select_autoescape(),  # Enable auto escaping.
        trim_blocks=True,  # Stops blocks from rendering a blank line.
        lstrip_blocks=True,  # Strips whitespace from in front of a block.
    )

    forecast_page_template = env.get_template("forecast_page.html.j2")
    about_template = env.get_template("about.html.j2")
    news_template = env.get_template("news.html.j2")

    forecast_page_contexts = get_forecast_page_contexts(areas, area_forecasts)

    # Index page is same as Ireland page
    index_context = forecast_page_contexts[0]
    about_context = get_about_page_context(areas)
    news_context = get_news_page_context(areas)

    # Note the encoding method, this returns a bytes string so these need to be written to files in
    # bytes mode
    forecast_page_outputs: List[bytes] = []
    for context in forecast_page_contexts:
        forecast_page_outputs.append(forecast_page_template.render(context).encode("utf8"))
    index_output = forecast_page_template.render(index_context).encode("utf8")
    about_output = about_template.render(about_context).encode("utf8")
    news_output = news_template.render(news_context).encode("utf8")

    for i, area in enumerate(areas):
        file_path = webpages_path.joinpath(f"{sanitize_name(area.name)}.html")
        with open(file_path, "wb") as file:
            file.write(forecast_page_outputs[i])

    index_file_path = webpages_path.joinpath("index.html")
    with open(index_file_path, "wb") as file:
        file.write(index_output)

    about_file_path = webpages_path.joinpath("about.html")
    with open(about_file_path, "wb") as file:
        file.write(about_output)

    news_file_path = webpages_path.joinpath("news.html")
    with open(news_file_path, "wb") as file:
        file.write(news_output)
