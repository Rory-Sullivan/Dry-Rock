import copy
import datetime as dt
import pathlib
from typing import Any, Dict, List, Optional, Tuple

import jinja2 as jinja
from metno_locationforecast import Forecast
from metno_locationforecast.data_containers import Variable

from ..places import Area
from .helper_functions import (
    UnitSystem,
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
                "href_metric": f"/pages/{sanitize_name(area.name)}_metric.html",
                "href_imperial": f"/pages/{sanitize_name(area.name)}_imperial.html",
                "is_active": False,
            }
        )
    nav_links.append(
        {
            "name": "About",
            "href_metric": "/pages/about_metric.html",
            "href_imperial": "/pages/about_imperial.html",
            "is_active": False,
        }
    )
    nav_links.append(
        {
            "name": "News",
            "href_metric": "/pages/news_metric.html",
            "href_imperial": "/pages/news_imperial.html",
            "is_active": False,
        }
    )
    return {"nav_links": nav_links}


def get_total_rain_for_interval(
    day: dt.date,
    start_time: dt.time,
    end_time: dt.time,
    forecast: Forecast,
) -> Variable | None:
    datetime_interval = (
        dt.datetime.combine(day, start_time, tzinfo=start_time.tzinfo),
        dt.datetime.combine(day, end_time, tzinfo=end_time.tzinfo),
    )
    relevant_intervals = forecast.data.intervals_between(datetime_interval[0], datetime_interval[1])
    total_rain = sum_rain(relevant_intervals) if len(relevant_intervals) > 0 else None

    return total_rain


def get_area_forecast_context(
    area: Area,
    place_forecasts: List[Forecast],
    days: List[dt.date],
    morning_times: List[dt.time],
    afternoon_times: List[dt.time],
    evening_times: List[dt.time],
) -> Dict[str, Any]:
    if len(area.places) != len(place_forecasts):
        raise ValueError("Number of places must match the number of place forecasts")

    context_forecasts = {}
    forecast_updated_at = {}
    for forecast in place_forecasts:
        forecasts_for_place: Dict[dt.date, Optional[object]] = {}
        for day in days:
            days_intervals = forecast.data.intervals_for(day, tzinfo=area.time_zone)

            if len(days_intervals) > 0:
                days_rain = sum_rain(days_intervals)
                days_max_temp = max_temp_of(days_intervals)
                days_min_temp = min_temp_of(days_intervals)
                days_max_wind_speed, days_max_wind_speed_direction = max_wind_speed_of(
                    days_intervals
                )

                morning_rain = get_total_rain_for_interval(
                    day, morning_times[0], morning_times[1], forecast
                )
                afternoon_rain = get_total_rain_for_interval(
                    day, afternoon_times[0], afternoon_times[1], forecast
                )
                evening_rain = get_total_rain_for_interval(
                    day, evening_times[0], evening_times[1], forecast
                )

                intervals: List[Dict[str, Any]] = []
                for day_interval in days_intervals:
                    interval: Dict[str, Any] = {
                        "start_time": day_interval.start_time.astimezone(area.time_zone),
                        "end_time": day_interval.end_time.astimezone(area.time_zone),
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
        forecast_updated_at[forecast.place.name] = forecast.data.updated_at.astimezone(
            area.time_zone
        )

    context: Dict[str, Any] = {
        "days": days,
        "places": area.places,
        "forecasts": context_forecasts,
        "updated_at": forecast_updated_at,
    }
    return context


def get_forecast_page_contexts(
    areas: List[Area], area_forecasts: List[List[Forecast]], unit_system: UnitSystem
) -> List[Dict[str, Any]]:
    """Returns a list of contexts one each per area for passing into the forecast page template."""

    if len(areas) != len(area_forecasts):
        raise ValueError("Number of areas must match the number of area forecasts")

    nav_bar_context = get_navbar_context(areas)

    # Copy forecasts and convert units to the relevant system
    area_forecasts = copy.deepcopy(area_forecasts)
    for place_forecasts in area_forecasts:
        change_units(place_forecasts, unit_system)

    forecast_page_contexts: List[Dict[str, Any]] = []
    for i, area in enumerate(areas):
        now = dt.datetime.now(area.time_zone)
        today = now.date()
        morning_times = [dt.time(6, tzinfo=area.time_zone), dt.time(11, 59, tzinfo=area.time_zone)]
        afternoon_times = [
            dt.time(12, tzinfo=area.time_zone),
            dt.time(17, 59, tzinfo=area.time_zone),
        ]
        evening_times = [dt.time(18, tzinfo=area.time_zone), dt.time(23, 59, tzinfo=area.time_zone)]
        days = [today + dt.timedelta(days=i) for i in range(7)]

        place_forecasts = area_forecasts[i]
        context = get_area_forecast_context(
            area, place_forecasts, days, morning_times, afternoon_times, evening_times
        )
        context["unit_system"] = unit_system.name
        context["nav_links"] = copy.deepcopy(nav_bar_context["nav_links"])
        context["nav_links"][i]["is_active"] = True
        context["units_nav_link"] = context["nav_links"][i]
        forecast_page_contexts.append(context)

    return forecast_page_contexts


def get_about_page_context(areas: List[Area]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    context_metric = get_navbar_context(areas)
    context_metric["nav_links"][len(areas)]["is_active"] = True
    context_metric["units_nav_link"] = context_metric["nav_links"][len(areas)]
    context_metric["unit_system"] = UnitSystem.METRIC.name

    context_imperial = copy.deepcopy(context_metric)
    context_imperial["unit_system"] = UnitSystem.IMPERIAL.name

    return context_metric, context_imperial


def get_news_page_context(areas: List[Area]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    context_metric = get_navbar_context(areas)
    context_metric["nav_links"][len(areas) + 1]["is_active"] = True
    context_metric["units_nav_link"] = context_metric["nav_links"][len(areas) + 1]
    context_metric["unit_system"] = UnitSystem.METRIC.name

    context_imperial = copy.deepcopy(context_metric)
    context_imperial["unit_system"] = UnitSystem.IMPERIAL.name

    return context_metric, context_imperial


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

    forecast_page_contexts_metric = get_forecast_page_contexts(
        areas, area_forecasts, UnitSystem.METRIC
    )
    forecast_page_contexts_imperial = get_forecast_page_contexts(
        areas, area_forecasts, UnitSystem.IMPERIAL
    )

    # Index page is same as metric Ireland page
    index_context = forecast_page_contexts_metric[0]
    about_context_metric, about_context_imperial = get_about_page_context(areas)
    news_context_metric, news_context_imperial = get_news_page_context(areas)

    # Note the encoding method, this returns a bytes string so these need to be written to files in
    # bytes mode
    forecast_page_outputs_metric: List[bytes] = []
    for context in forecast_page_contexts_metric:
        forecast_page_outputs_metric.append(forecast_page_template.render(context).encode("utf8"))
    forecast_page_outputs_imperial: List[bytes] = []
    for context in forecast_page_contexts_imperial:
        forecast_page_outputs_imperial.append(forecast_page_template.render(context).encode("utf8"))
    index_output = forecast_page_template.render(index_context).encode("utf8")
    about_output_metric = about_template.render(about_context_metric).encode("utf8")
    about_output_imperial = about_template.render(about_context_imperial).encode("utf8")
    news_output_metric = news_template.render(news_context_metric).encode("utf8")
    news_output_imperial = news_template.render(news_context_imperial).encode("utf8")

    for i, area in enumerate(areas):
        file_path_metric = webpages_path.joinpath(f"{sanitize_name(area.name)}_metric.html")
        with open(file_path_metric, "wb") as file:
            file.write(forecast_page_outputs_metric[i])
        file_path_imperial = webpages_path.joinpath(f"{sanitize_name(area.name)}_imperial.html")
        with open(file_path_imperial, "wb") as file:
            file.write(forecast_page_outputs_imperial[i])

    index_file_path = webpages_path.joinpath("index.html")
    with open(index_file_path, "wb") as file:
        file.write(index_output)

    about_file_path_metric = webpages_path.joinpath("about_metric.html")
    with open(about_file_path_metric, "wb") as file:
        file.write(about_output_metric)
    about_file_path_imperial = webpages_path.joinpath("about_imperial.html")
    with open(about_file_path_imperial, "wb") as file:
        file.write(about_output_imperial)

    news_file_path_metric = webpages_path.joinpath("news_metric.html")
    with open(news_file_path_metric, "wb") as file:
        file.write(news_output_metric)
    news_file_path_imperial = webpages_path.joinpath("news_imperial.html")
    with open(news_file_path_imperial, "wb") as file:
        file.write(news_output_imperial)
