"""Updates weather data for all places and renders templates."""

import logging
import pathlib
from typing import List

from metno_locationforecast import Forecast

from .config import AREAS_FILE, LOGGING_LEVEL, OUTPUT_PATH
from .copy_reports import copy_index
from .places import get_areas
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

    areas = get_areas(AREAS_FILE)
    logger.debug("Got all areas")

    area_forecasts: List[List[Forecast]] = []
    for area in areas:
        place_forecasts: List[Forecast] = []
        for place in area.places:
            place_forecasts.append(Forecast(place))

        area_forecasts.append(place_forecasts)

    for area_forecast in area_forecasts:
        for place_forecast in area_forecast:
            status = place_forecast.update()
            if status == "Data-Modified":
                logger.debug(f"Forecast data for {place_forecast.place.name} updated")
            if hasattr(place_forecast, "response") and (
                status_code := place_forecast.response.status_code
            ) not in {
                200,
                304,
            }:
                logger.warning(
                    f"Received {status_code} response for request to update {place_forecast.place.name} data"  # noqa: E501
                )

    logger.debug("Updated all forecasts")

    render_html_pages(areas, area_forecasts)
    copy_index()

    logger.info("Completed update")
