"""
Set up our weather reports.
"""
import datetime as dt
import os

import requests
from bs4 import BeautifulSoup

from dryrock.forecasts.data_containers import (
    Forecast,
    ForecastInterval,
    Variable,
    WindVariable,
)
from dryrock.places import Place


class YrForecast(Forecast):
    """ Class for storing a forecast from Yr. """

    def __init__(
        self,
        forecast_type: str,
        place: Place,
        updated_at: dt.datetime,
        valid_until: dt.datetime,
        sunrise: dt.datetime,
        sunset: dt.datetime,
        intervals: list,
    ):
        name = f"Yr {forecast_type} for {place.name}"
        super().__init__(name, place, updated_at, valid_until, intervals)
        self.sunrise = sunrise
        self.sunset = sunset


class YrData:
    """ Class for storing Yr data. """

    website = "http://yr.no/en"

    cite_text = (
        "Weather forecast from Yr, delivered by the Norwegian "
        + "Meteorological Institute and the NRK"
    )

    def __init__(self, date: dt.datetime, place: Place, output_path: str):
        self.name = f"Yr data for {place.name}"
        self.date = date
        self.place = place

        self.xml_path = output_path.joinpath("yr_xml_forecasts/")

        self.long_range_forecast = self.create_forecast(place, "lr")
        self.hour_by_hour_forecast = self.create_forecast(place, "hbh")

    def yr_get_xml_file(self, place: Place, forecast_type: str):
        """
        Method for retrieving a Yr xml file.  Returns the file name.

        Forecast type can be long range 'lr' or hour by hour 'hbh'
        """

        if not os.path.isdir(self.xml_path):
            os.mkdir(self.xml_path)

        if forecast_type == "lr":
            url = f"{place.yr_url}forecast.xml"
            file_name = f"{self.xml_path}{place.name}_lr_forecast.xml"
        elif forecast_type == "hbh":
            url = f"{place.yr_url}forecast_hour_by_hour.xml"
            file_name = f"{self.xml_path}{place.name}_hbh_forecast.xml"
        else:
            raise Exception(f"{forecast_type} is not a valid forecast type.")

        source = requests.get(url).text
        with open(file_name, "w", newline="") as file:
            file.write(source)

        print(f"Got {forecast_type} for {place.name}")
        return file_name, forecast_type, place

    @staticmethod
    def yr_xml_to_forecast(file_name, forecast_type, place) -> YrForecast:
        """ Method for producing  a Yr forecast from a Yr xml files soup. """

        with open(file_name) as file:
            source = file.read()

        soup = BeautifulSoup(source, "xml")

        updated_at = soup.find("lastupdate").text
        updated_at = dt.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S")

        valid_until = soup.find("nextupdate").text
        valid_until = dt.datetime.strptime(valid_until, "%Y-%m-%dT%H:%M:%S")

        sun_times = soup.find("sun")
        sunrise = sun_times["rise"]
        sunrise = dt.datetime.strptime(sunrise, "%Y-%m-%dT%H:%M:%S")
        sunset = sun_times["set"]
        sunset = dt.datetime.strptime(sunset, "%Y-%m-%dT%H:%M:%S")

        intervals = []

        for interval in soup.find_all("time"):
            start_time = dt.datetime.strptime(
                interval["from"], "%Y-%m-%dT%H:%M:%S"
            )
            end_time = dt.datetime.strptime(interval["to"], "%Y-%m-%dT%H:%M:%S")

            precip_value = float(interval.find("precipitation")["value"])
            wind_direction = interval.find("windDirection")["name"]
            wind_value = float(interval.find("windSpeed")["mps"])
            temperature_value = float(interval.find("temperature")["value"])
            temperature_unit = interval.find("temperature")["unit"]

            interval_variables = {
                "precipitation": Variable("Rain", precip_value, "mm"),
                "wind": WindVariable(wind_value, "mps", wind_direction),
                "temperature": Variable(
                    "Temperature", temperature_value, temperature_unit
                ),
            }

            intervals.append(
                ForecastInterval(start_time, end_time, interval_variables)
            )

        # print(f"Yr forecast of {file_name} updated.")
        return YrForecast(
            forecast_type,
            place,
            updated_at,
            valid_until,
            sunrise,
            sunset,
            intervals,
        )

    def create_forecast(self, place: Place, forecast_type: str) -> YrForecast:
        """
        Creates a forecast.
        """

        if forecast_type == "lr":
            file_name = f"{self.xml_path}{place.name}_lr_forecast.xml"
        elif forecast_type == "hbh":
            file_name = f"{self.xml_path}{place.name}_hbh_forecast.xml"
        else:
            raise Exception(f"{forecast_type} is not a valid forecast type.")

        if not os.path.isfile(file_name):
            self.yr_get_xml_file(place, forecast_type)

        # print(f"Created {forecast_type} for {place.name}")
        return YrData.yr_xml_to_forecast(file_name, forecast_type, place)

    def update_long_range_forecast(self):
        """
        Method for retrieving the Yr long range forecasts.

        These forecasts are in 6 hour intervals for the next 9 days.
        """

        if dt.datetime.now() >= self.long_range_forecast.valid_until:
            print(f"Updating lr forecast for {self.name}")
            forecast_file_name, forecast_type, place = self.yr_get_xml_file(
                self.place, "lr"
            )
            self.long_range_forecast = self.yr_xml_to_forecast(
                forecast_file_name, forecast_type, place
            )
        else:
            # print("Forecast is still valid. Valid until " +
            # f"{self.long_range_forecast.valid_until}")
            pass

        return

    def update_hour_by_hour_forecast(self):
        """ Method for retrieving the Yr hour by hour forecasts. """

        if dt.datetime.now() >= self.hour_by_hour_forecast.valid_until:
            # print(f"Updating hbh forecast for {self.name}")
            forecast_file_name, forecast_type, place = self.yr_get_xml_file(
                self.place, "hbh"
            )
            self.hour_by_hour_forecast = self.yr_xml_to_forecast(
                forecast_file_name, forecast_type, place
            )
        else:
            # print("Forecast is still valid. Valid until " +
            # f"{self.hour_by_hour_forecast.valid_until}")
            pass

        return
