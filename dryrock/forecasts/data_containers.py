"""
Classes for holding different pieces of data related to weather forecasts.
"""
import datetime as dt

from dryrock.places import Place


class Variable:
    """Stores data for weather variables, e.g. rain, temperature."""

    def __init__(self, name: str, value: float, unit: str):
        self.name = name
        self.value = value
        self.unit = unit

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit}"


class WindVariable(Variable):
    """Special variable class for storing wind data."""

    def __init__(self, value: float, unit: str, direction: str):
        super().__init__("Wind", value, unit)
        self.direction = direction

    def __str__(self):
        return (
            f"{self.name}: {self.value} {self.unit} from a {self.direction} "
            + "direction"
        )

    def convert_mps_to_kph(self):
        """Function for converting wind variable from meters per second to
        kilometers per hour.

        Will raise a value error if unit value is not 'mps' or 'kph'.
        """

        if self.unit == "mps":
            self.unit = "kph"
            self.value = (self.value * 360) / 100

        elif self.unit == "kph":
            pass

        else:
            raise ValueError(
                "Not a valid unit conversion units must be 'mps' or 'kph'."
            )


class ForecastInterval:
    """Stores information for an interval of a forecast, contains variables."""

    def __init__(
        self, start_time: dt.datetime, end_time: dt.datetime, variables: dict
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.variables_dict = variables

    def __str__(self):
        string = f"Forecast between: {self.start_time} and {self.end_time}"
        for variable in self.variables_dict.values():
            string += f"\n{str(variable)}"
        return string


class Forecast:
    """Class for storing a forecast.  This is a group of forecast intervals."""

    def __init__(
        self,
        name: str,
        place: Place,
        updated_at: dt.datetime,
        valid_until: dt.datetime,
        forecast_intervals: list,
    ):
        self.name = name
        self.place = place
        self.updated_at = updated_at
        self.valid_until = valid_until
        self.intervals = forecast_intervals

    def get_relevant_intervals(self, day: dt.date):
        """Returns the relevant intervals for specified day."""

        relevant_date = day
        relevant_intervals = []

        for interval in self.intervals:
            if interval.start_time.date() == relevant_date:
                relevant_intervals.append(interval)

        return relevant_intervals

    @property
    def tomorrows_intervals(self):
        """ Get just tomorrows intervals. """
        tomorrow = dt.date.today() + dt.timedelta(days=1)
        return self.get_relevant_intervals(tomorrow)

    @property
    def saturdays_intervals(self):
        """ Get intervals for the next Saturday. """
        next_saturday = dt.date.today() + dt.timedelta(
            days=1
        )  # Ensures we move to the next week.
        while (
            next_saturday.weekday() != 5
        ):  # Relevant number for the day we want.
            next_saturday += dt.timedelta(days=1)
        return self.get_relevant_intervals(next_saturday)

    @property
    def sundays_intervals(self):
        """ Get intervals for the next Sunday. """

        next_sunday = dt.date.today() + dt.timedelta(days=1)
        while next_sunday.weekday() != 6:
            next_sunday += dt.timedelta(days=1)
        return self.get_relevant_intervals(next_sunday)


# Code for combining forecasts.
# t_times = []
#         end_times = []
#         precipitation = 0
#         temperatures = []
#         wind_speeds = []
#         wind_directions = []
#         temperature_unit = "celsius"
#
#         # Combine forecasts.
#         for forecast in relevant_forecasts:
#             start_times.append(forecast.start_time)
#             end_times.append(forecast.end_time)
#             precipitation += forecast.variables_dict["precipitation"].value
#             temperatures.append(forecast.variables_dict["temperature"].value)
#             wind_speeds.append(forecast.variables_dict["wind"].value)
#             wind_directions.append(forecast.variables_dict["wind"].direction)
#
#         start_time = min(start_times)
#         end_time = max(end_times)
#         # precipitation is the sum of all precipitations
#         min_temp = min(temperatures)
#         max_temp = max(temperatures)
#         wind_speed = max(wind_speeds)
#         wind_direction = wind_directions[0]
#         for i in range(len(wind_speeds)):  # Find the wind direction
# corresponding to the wind speed.
#             if wind_speed == wind_speeds[i]:
#                 wind_direction = wind_directions[i]
#
#         variables_dict = {
#             "precipitation": Variable("Rain", precipitation, "mm"),
#             "wind": WindVariable(wind_speed, "mps", wind_direction),
#             "max_temp": Variable("Max temperature", max_temp,
# temperature_unit),
#             "min_temp": Variable("Min temperature", min_temp,
# temperature_unit)
#         }
