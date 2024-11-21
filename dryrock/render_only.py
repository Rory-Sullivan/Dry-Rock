"""Renders all of the HTML files from current data."""

from typing import List

from config import AREAS_FILE
from copy_reports import copy_index
from metno_locationforecast import Forecast
from places import get_areas
from reports.render_html import render_html_pages

if __name__ == "__main__":
    areas = get_areas(AREAS_FILE)

    area_forecasts: List[List[Forecast]] = []
    for area in areas:
        place_forecasts: List[Forecast] = []
        for place in area.places:
            place_forecasts.append(Forecast(place))

        area_forecasts.append(place_forecasts)

    for area_forecast in area_forecasts:
        for place_forecast in area_forecast:
            place_forecast.load()

    render_html_pages(areas, area_forecasts)
    copy_index()
