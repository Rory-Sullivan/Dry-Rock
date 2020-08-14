"""Renders all of the HTML files from current data."""

from typing import List

from metno_locationforecast import Forecast

from .config import PLACES_FILE
from .copy_reports import copy_index
from .places import get_places
from .reports.render_html import render_html_pages

if __name__ == "__main__":
    places = get_places(PLACES_FILE)

    forecasts: List[Forecast] = []
    for place in places:
        forecasts.append(Forecast(place))

    for forecast in forecasts:
        forecast.load()

    render_html_pages(forecasts)
    copy_index()
