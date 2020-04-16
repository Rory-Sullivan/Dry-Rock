"""
Set up our weather reports.
"""
import datetime as dt
import os

import requests
from bs4 import BeautifulSoup

from general_classes import (
    Forecast,
    Place,
    ForecastInterval,
    Variable,
    WindVariable,
)


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
    xml_path = "yr_xml_forecasts/"
    if not os.path.isdir(xml_path):
        os.mkdir(xml_path)

    cite_text = (
        "Weather forecast from Yr, delivered by the Norwegian "
        + "Meteorological Institute and the NRK"
    )

    def __init__(self, date: dt.datetime, place: Place):
        self.name = f"Yr data for {place.name}"
        self.date = date
        self.place = place

        self.long_range_forecast = YrData.create_forecast(place, "lr")
        self.hour_by_hour_forecast = YrData.create_forecast(place, "hbh")

    @staticmethod
    def yr_get_xml_file(place: Place, forecast_type: str):
        """
        Method for retrieving a Yr xml file.  Returns the file name.

        Forecast type can be long range 'lr' or hour by hour 'hbh'
        """

        if forecast_type == "lr":
            url = f"{place.yr_url}forecast.xml"
            file_name = f"{YrData.xml_path}{place.name}_lr_forecast.xml"
        elif forecast_type == "hbh":
            url = f"{place.yr_url}forecast_hour_by_hour.xml"
            file_name = f"{YrData.xml_path}{place.name}_hbh_forecast.xml"
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

    @staticmethod
    def create_forecast(place: Place, forecast_type: str) -> YrForecast:
        """
        Creates a forecast.
        """

        if forecast_type == "lr":
            file_name = f"{YrData.xml_path}{place.name}_lr_forecast.xml"
        elif forecast_type == "hbh":
            file_name = f"{YrData.xml_path}{place.name}_hbh_forecast.xml"
        else:
            raise Exception(f"{forecast_type} is not a valid forecast type.")

        if not os.path.isfile(file_name):
            YrData.yr_get_xml_file(place, forecast_type)

        # print(f"Created {forecast_type} for {place.name}")
        return YrData.yr_xml_to_forecast(file_name, forecast_type, place)

    def update_long_range_forecast(self):
        """
        Method for retrieving the Yr long range forecasts.

        These forecasts are in 6 hour intervals for the next 9 days.
        """

        if dt.datetime.now() >= self.long_range_forecast.valid_until:
            print(f"Updating lr forecast for {self.name}")
            forecast_file_name, forecast_type, place = YrData.yr_get_xml_file(
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
            forecast_file_name, forecast_type, place = YrData.yr_get_xml_file(
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

    # TODO: overwrite this in weather data.
    def yr_create_text_report(self) -> str:
        """ Method for creating a text report. """

        text = ""

        text += f"Yr forecast for {self.place.name}\n"
        text += f"Updated at : {self.long_range_forecast.updated_at}\n"

        # Add text for tomorrows forecast.
        # tomorrows_forecast = self.hour_by_hour_forecast
        tomorrows_forecast = self.long_range_forecast
        tomorrows_intervals = tomorrows_forecast.tomorrows_intervals

        if len(tomorrows_intervals) == 0:
            text += "No forecast for tomorrow.\n"

        else:
            text += "\n"
            text += f"Tomorrow - {tomorrows_intervals[0].start_time.date()}\n"
            text += (
                f"Sunrise: {tomorrows_forecast.sunrise.time()}    "
                + "Sunset: {tomorrows_forecast.sunset.time()}\n"
            )

            for interval in tomorrows_intervals:
                text += f"{interval.start_time.time()} "
                text += "{} ".format(
                    str(interval.variables_dict["precipitation"])
                )
                text += "{} \n".format(
                    str(interval.variables_dict["temperature"])
                )
                text += "         {} ".format(
                    str(interval.variables_dict["wind"])
                )
                text += "\n"

        text += "\n"

        # Add text for next Saturdays forecast.
        # saturdays_forecast = self.hour_by_hour_forecast
        saturdays_forecast = self.long_range_forecast
        saturdays_intervals = saturdays_forecast.saturdays_intervals

        if len(saturdays_intervals) == 0:
            text += "No forecasts for Saturday.\n"

        else:
            text += f"Saturday - {saturdays_intervals[0].start_time.date()}\n"
            # text += f"Sunrise: {saturdays_forecast.sunrise.time()}    "
            # + "Sunset: {saturdays_forecast.sunset.time()}\n"

            for interval in saturdays_intervals:
                text += f"{interval.start_time.time()} "
                text += "{} ".format(
                    str(interval.variables_dict["precipitation"])
                )
                text += "{} \n".format(
                    str(interval.variables_dict["temperature"])
                )
                text += "         {} ".format(
                    str(interval.variables_dict["wind"])
                )
                text += "\n"

        text += "\n"

        # Add text for next Sundays forecast.
        # sundays_forecast = self.hour_by_hour_forecast
        sundays_forecast = self.long_range_forecast
        sundays_intervals = sundays_forecast.sundays_intervals

        if len(sundays_intervals) == 0:
            text += "No forecasts for Sunday.\n"

        else:
            text += f"Sunday - {sundays_intervals[0].start_time.date()}\n"
            # text += f"Sunrise: {sundays_forecast.sunrise.time()}    "
            # + "Sunset: {sundays_forecast.sunset.time()}\n"

            for interval in sundays_intervals:
                text += f"{interval.start_time.time()} "
                text += "{} ".format(
                    str(interval.variables_dict["precipitation"])
                )
                text += "{} \n".format(
                    str(interval.variables_dict["temperature"])
                )
                text += "         {} ".format(
                    str(interval.variables_dict["wind"])
                )
                text += "\n"

        return text
