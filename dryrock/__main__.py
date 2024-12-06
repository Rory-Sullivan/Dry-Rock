"""Updates weather data for all places and renders templates."""

import logging
import pathlib
import sys
from typing import List

from metno_locationforecast import Forecast

from .config import AREAS_FILE, LOGGING_LEVEL, OUTPUT_PATH
from .copy_reports import copy_index
from .places import get_areas
from .reports.render_html import render_html_pages

if __name__ == "__main__":

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(LOGGING_LEVEL)
    file_handler = logging.FileHandler("dryrock.log")
    file_handler.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Check for render only mode (passed as a command line parameter)
    render_only = False
    if "--render-only" in sys.argv:
        render_only = True
        logger.warning("Running in render only mode")

    # Output path
    output_path = pathlib.Path(OUTPUT_PATH)
    logger.info(f"Outputting files to: {output_path}")
    if not output_path.is_dir():
        logger.debug("Output file path does not exist, creating output file path")
        output_path.mkdir(parents=True)

    # Load areas from areas file
    logger.info("Loading areas")
    areas = get_areas(AREAS_FILE)
    logger.debug("Loaded areas")

    logger.info("Creating forecasts")
    area_forecasts: List[List[Forecast]] = []
    for area in areas:
        place_forecasts: List[Forecast] = []
        for place in area.places:
            place_forecasts.append(Forecast(place))

        area_forecasts.append(place_forecasts)
    logger.debug("Created areas")

    if not render_only:
        # Check for updated weather data
        logger.info("Updating forecasts")
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
        logger.debug("Updated forecasts")
    else:
        # Load weather data from files
        logger.info("Loading forecasts from existing data")
        for area_forecast in area_forecasts:
            for place_forecast in area_forecast:
                place_forecast.load()
        logger.debug("Loaded forecasts from existing data")

    # Render HTML pages
    logger.info("Rendering pages")
    render_html_pages(areas, area_forecasts)
    copy_index()
    logger.debug("Rendered pages")

    logger.info("Complete")
