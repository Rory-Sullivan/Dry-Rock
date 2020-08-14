"""Updates weather data for all places and renders templates."""

import logging
import pathlib
from typing import List

from metno_locationforecast import Forecast

from .config import OUTPUT_PATH, PLACES_FILE, LOGGING_LEVEL
from .copy_reports import copy_index
from .places import get_places
from .reports.render_html import render_html_pages

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.setLevel(LOGGING_LEVEL)
    file_handler = logging.FileHandler("dryrock.log")
    file_handler.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    output_path = pathlib.Path(OUTPUT_PATH)

    if not output_path.is_dir():
        output_path.mkdir(parents=True)

    logger.info("Starting data collection")

    places = get_places(PLACES_FILE)
    logger.debug("Got all places")

    forecasts: List[Forecast] = []
    for place in places:
        forecasts.append(Forecast(place))

    for forecast in forecasts:
        status = forecast.update()
        if status == "Data-Modified":
            logger.debug(f"Forecast data for {forecast.place.name} updated")
        if hasattr(forecast, "response") and (status_code := forecast.response.status_code) not in {
            200,
            304,
        }:
            logger.warning(
                f"Received {status_code} response for request to update {forecast.place.name} data"
            )

    logger.debug("Updated all forecasts")

    render_html_pages(forecasts)
    copy_index()

    logger.info("Completed update")
