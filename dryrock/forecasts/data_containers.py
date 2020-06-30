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
        return f"{self.value} {self.unit}"


class TempVariable(Variable):
    """Special variable class for storing temperature data."""

    def __str__(self):
        if self.unit == "celsius":
            return f"{self.value} &deg;C"
        if self.unit == "fahrenheit":
            return f"{self.value} &deg;F"
        return super().__str__()


class WindVariable(Variable):
    """Special variable class for storing wind data."""

    def __init__(self, value: float, unit: str, direction: str):
        super().__init__("Wind", value, unit)
        self.direction = direction

    def __str__(self):
        return f"{self.value} {self.unit} from a {self.direction} direction"

    def convert_mps_to_kph(self):
        """Function for converting wind variable from meters per second to
        kilometers per hour.

        Will raise a value error if unit value is not 'mps' or 'kph'.
        """

        if self.unit == "mps":
            self.unit = "kph"
            self.value = ((self.value * 360) / 100).__round__(2)

        elif self.unit == "kph":
            pass

        else:
            raise ValueError("Not a valid unit conversion units must be 'mps' or 'kph'.")


class ForecastInterval:
    """Stores information for an interval of a forecast, contains variables."""

    def __init__(
        self, start_time: dt.datetime, end_time: dt.datetime, time_period: int, variables: dict
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.time_period = time_period
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

    def get_relevant_intervals(self, day: dt.date) -> list:
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
        next_saturday = dt.date.today() + dt.timedelta(days=1)  # Ensures we move to the next week.
        while next_saturday.weekday() != 5:  # Relevant number for the day we want.
            next_saturday += dt.timedelta(days=1)
        return self.get_relevant_intervals(next_saturday)

    @property
    def sundays_intervals(self):
        """ Get intervals for the next Sunday. """

        next_sunday = dt.date.today() + dt.timedelta(days=1)
        while next_sunday.weekday() != 6:
            next_sunday += dt.timedelta(days=1)
        return self.get_relevant_intervals(next_sunday)
