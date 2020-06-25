"""
Code for handling the gathering of our weather data.
"""
import datetime as dt
import os


from dryrock.forecasts.yr import YrData


class WeatherData:
    """ Class for gathering and storing all of our weather data. """

    def __init__(self, date: dt.datetime, places: list, output_path):

        self.date = date
        self.places = places

        # Collect information from Yr.
        self.yr_data_for_places = {}

        for place in self.places:
            yr_data_for_place = YrData(date, place, output_path)

            # ------------------------------------------------------------------
            # Set which forecast we want to use.
            # ------------------------------------------------------------------
            yr_data_for_place.update_long_range_forecast()
            # yr_data_for_place.update_hour_by_hour_forecast()

            self.yr_data_for_places[place.name] = yr_data_for_place


class WeatherDataNoUpdate:
    """ Class for gathering and storing all of our weather data. """

    def __init__(self, date: dt.datetime, places: list, output_path):

        self.date = date
        self.places = places

        # Collect information from Yr.
        self.yr_data_for_places = {}

        for place in self.places:
            yr_data_for_place = YrData(date, place, output_path)

            # ------------------------------------------------------------------
            # Set which forecast we want to use.
            # ------------------------------------------------------------------
            # yr_data_for_place.update_long_range_forecast()
            # yr_data_for_place.update_hour_by_hour_forecast()

            self.yr_data_for_places[place.name] = yr_data_for_place


# For testing our code.
# if __name__ == "__main__":
#     from general_classes import Place

#     TEST_WEATHER_DATA = WeatherData(
#         dt.datetime.now(),
#         [
#             Place(
#                 "Dublin",
#                 "Ireland/Leinster/Dublin",
#                 "https://www.yr.no/en/forecast/daily-table/2-2964574",
#             )
#         ],
#     )

#     TEST_WEATHER_DATA.update_html_report()
