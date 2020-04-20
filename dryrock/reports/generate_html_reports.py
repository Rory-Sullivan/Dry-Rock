from copy import deepcopy
import pathlib

import jinja2 as jinja

from dryrock.forecasts.combined import WeatherData
from dryrock.forecasts.yr import YrData


def update_html_report(data: WeatherData, output_path: pathlib.Path):
    """ Updates index.html """

    reports_path = output_path.joinpath("webpages/")

    if not reports_path.exists():
        reports_path.mkdir(parents=True)

    file_path = reports_path.joinpath(f"index.html")

    # Set up our variables to make them easy to use in our template.
    context = []

    # Variables used for calculating place with least rain.
    tom_total_rains = {}
    sat_total_rains = {}
    sun_total_rains = {}

    for place in data.places:
        # ------------------------------------------------------------------
        # Set relevant forecast.
        # ------------------------------------------------------------------
        relevant_forecast = data.yr_data_for_places[
            place.name
        ].long_range_forecast

        tom_intervals_for_place = deepcopy(
            relevant_forecast.tomorrows_intervals
        )
        sat_intervals_for_place = deepcopy(
            relevant_forecast.saturdays_intervals
        )
        sun_intervals_for_place = deepcopy(relevant_forecast.sundays_intervals)

        # Set how to display our variables.
        tomorrows_date = tom_intervals_for_place[0].start_time.strftime("%d %B")
        saturdays_date = sat_intervals_for_place[0].start_time.strftime("%d %B")
        sundays_date = sun_intervals_for_place[0].start_time.strftime("%d %B")

        total_rains = []

        for intervals in [
            tom_intervals_for_place,
            sat_intervals_for_place,
            sun_intervals_for_place,
        ]:
            total_rain = 0.0

            for interval in intervals:

                # Display for start time.
                interval.start_time = interval.start_time.strftime("%H:%M")

                # Display for temperature.
                if interval.variables_dict["temperature"].unit == "celsius":
                    interval.variables_dict["temperature"].unit = "&degC"
                else:
                    interval.variables_dict["temperature"].unit = "unknown"

                # Display for wind.
                interval.variables_dict["wind"].convert_mps_to_kph()
                interval.variables_dict["wind"].value = round(
                    interval.variables_dict["wind"].value
                )

                # Calculate total rain fall.
                total_rain += interval.variables_dict["precipitation"].value

            total_rains.append(total_rain)

        tom_total_rains[place.name] = round(total_rains[0], 1)
        sat_total_rains[place.name] = round(total_rains[1], 1)
        sun_total_rains[place.name] = round(total_rains[2], 1)

        info_for_place = {
            "name": place.name,
            "yr_link": place.yr_link,
            "cite_yr": YrData.cite_text,
            "updated_at": relevant_forecast.updated_at.strftime(
                "%d/%m/%y %H:%M"
            ),
            "sunrise_time": relevant_forecast.sunrise.strftime("%H:%M"),
            "sunset_time": relevant_forecast.sunset.strftime("%H:%M"),
            "tomorrows_date": tomorrows_date,
            "tomorrows_intervals": tom_intervals_for_place,
            "saturdays_date": saturdays_date,
            "saturdays_intervals": sat_intervals_for_place,
            "sundays_date": sundays_date,
            "sundays_intervals": sun_intervals_for_place,
        }
        context.append(info_for_place)

    #  Here we calculate the least rainy place for each day.
    tom_total_rains["least rain"] = min(
        tom_total_rains, key=tom_total_rains.get
    )
    sat_total_rains["least rain"] = min(
        sat_total_rains, key=sat_total_rains.get
    )
    sun_total_rains["least rain"] = min(
        sun_total_rains, key=sun_total_rains.get
    )

    total_rains = [tom_total_rains, sat_total_rains, sun_total_rains]

    # Set up our environment.
    env = jinja.Environment(
        loader=jinja.FileSystemLoader("./dryrock/reports/templates"),
        autoescape=jinja.select_autoescape(),  # Enable auto escaping.
        trim_blocks=True,  # Stops blocks from rendering a blank line.
        lstrip_blocks=True,  # Strips whitespace from in front of a block.
    )

    # Import template.
    template = env.get_template("report_template.html")

    # Render the template.
    output = template.render(context=context, total_rains=total_rains)

    with open(file_path, "w") as file:
        file.write(output)
