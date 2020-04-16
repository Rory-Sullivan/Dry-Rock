"""
Code for handling the gathering of our weather data and creation of reports to
be emailed.
"""
import datetime as dt
import os
from copy import deepcopy

from jinja2 import Environment, FileSystemLoader, select_autoescape
from helpers.yr import YrData


class WeatherData:
    """ Class for gathering and storing all of our weather data. """

    reports_path = "./data/output/reports/"
    if not os.path.isdir(reports_path):
        os.mkdir(reports_path)

    def __init__(self, date: dt.datetime, places: list):

        self.date = date
        self.places = places

        # Collect information from Yr.
        self.yr_data_for_places = {}

        for place in self.places:
            yr_data_for_place = YrData(date, place)

            # ------------------------------------------------------------------
            # Set which forecast we want to use.
            # ------------------------------------------------------------------
            yr_data_for_place.update_long_range_forecast()
            # yr_data_for_place.update_hour_by_hour_forecast()

            self.yr_data_for_places[place.name] = yr_data_for_place

    def update_text_report(self):
        """ Updates the data in our txt file. """

        file_name = f"{WeatherData.reports_path}text_report.txt"

        with open(file_name, "w") as file:

            for place in self.places:
                yr_data_for_place = self.yr_data_for_places[place.name]
                text_report = yr_data_for_place.yr_create_text_report()
                file.write(text_report)
        return

    def update_html_report(self):
        """ Updates the data in our html file. """

        file_name = f"{WeatherData.reports_path}html_report.html"

        # Set up our variables to make them easy to use in our template.
        context = []

        # Variables used for calculating place with least rain.
        tom_total_rains = {}
        sat_total_rains = {}
        sun_total_rains = {}

        for place in self.places:
            # ------------------------------------------------------------------
            # Set relevant forecast.
            # ------------------------------------------------------------------
            relevant_forecast = self.yr_data_for_places[
                place.name
            ].long_range_forecast

            tom_intervals_for_place = deepcopy(
                relevant_forecast.tomorrows_intervals
            )
            sat_intervals_for_place = deepcopy(
                relevant_forecast.saturdays_intervals
            )
            sun_intervals_for_place = deepcopy(
                relevant_forecast.sundays_intervals
            )

            # Set how to display our variables.
            tomorrows_date = tom_intervals_for_place[0].start_time.strftime(
                "%d %B"
            )
            saturdays_date = sat_intervals_for_place[0].start_time.strftime(
                "%d %B"
            )
            sundays_date = sun_intervals_for_place[0].start_time.strftime(
                "%d %B"
            )

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
        env = Environment(
            loader=FileSystemLoader(
                "./dry_rock/templates"
            ),  # Loads templates from our templates directory.
            autoescape=select_autoescape(),  # Enable auto escaping.
            trim_blocks=True,  # Stops blocks from rendering a blank line.
            lstrip_blocks=True,  # Strips whitespace from in front of a block.
        )

        # Import template.
        template = env.get_template("report_template.html")

        # Render the template.
        output = template.render(context=context, total_rains=total_rains)

        with open(file_name, "w") as file:
            file.write(output)

        return


# For testing our code.
if __name__ == "__main__":
    from general_classes import Place

    TEST_WEATHER_DATA = WeatherData(
        dt.datetime.now(),
        [
            Place(
                "Dublin",
                "Ireland/Leinster/Dublin",
                "https://www.yr.no/en/forecast/daily-table/2-2964574",
            )
        ],
    )

    TEST_WEATHER_DATA.update_html_report()
