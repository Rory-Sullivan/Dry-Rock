from typing import List, Tuple

from metno_locationforecast import Forecast
from metno_locationforecast.data_containers import Interval, Variable


def cardinal_name_of(direction_variable: Variable) -> str:
    assert direction_variable.name == "wind_from_direction"
    assert direction_variable.units == "degrees"

    value = direction_variable.value
    if (337.5 <= value <= 360) or (0 <= value < 22.5):
        return "North"
    if 22.5 <= value < 67.5:
        return "Northeast"
    if 67.5 <= value < 112.5:
        return "East"
    if 112.5 <= value < 157.5:
        return "Southeast"
    if 157.5 <= value < 202.5:
        return "South"
    if 202.5 <= value < 247.5:
        return "Southwest"
    if 247.5 <= value < 292.5:
        return "West"
    if 292.5 <= value < 337.5:
        return "Northwest"
    raise RuntimeError(
        f"cardinal_name_of has failed with input {direction_variable} and value {value}."
    )


def sum_rain(intervals: List[Interval]) -> Variable:
    if len(intervals) > 0:
        total_rain = Variable("precipitation_amount", 0.0, "mm")
        for interval in intervals:
            total_rain += interval.variables["precipitation_amount"]
        return total_rain
    raise IndexError("Intervals cannot be empty.")


def max_temp_of(intervals: List[Interval]) -> Variable:
    if len(intervals) > 0:
        max_temp = Variable("air_temperature", float("-inf"), "celsius")
        for interval in intervals:
            if max_temp.value < interval.variables["air_temperature"].value:
                max_temp = interval.variables["air_temperature"]
        return max_temp
    raise IndexError("Intervals connot be empty.")


def min_temp_of(intervals: List[Interval]) -> Variable:
    if len(intervals) > 0:
        min_temp = Variable("air_temperature", float("inf"), "celsius")
        for interval in intervals:
            if min_temp.value > interval.variables["air_temperature"].value:
                min_temp = interval.variables["air_temperature"]
        return min_temp
    raise IndexError("Intervals connot be empty.")


def max_wind_speed_of(intervals: List[Interval]) -> Tuple[Variable, Variable]:
    if len(intervals) > 0:
        max_wind_speed = Variable("wind_speed", float("-inf"), "m/s")
        max_wind_speed_direction = Variable("wind_from_direction", 0.0, "degrees")
        for interval in intervals:
            if max_wind_speed.value < interval.variables["wind_speed"].value:
                max_wind_speed = interval.variables["wind_speed"]
                max_wind_speed_direction = interval.variables["wind_from_direction"]
        return max_wind_speed, max_wind_speed_direction
    raise IndexError("Intervals connot be empty.")


def change_units(forecasts: List[Forecast]) -> None:
    """Change wind speed to km/h."""

    for forecast in forecasts:
        for interval in forecast.data.intervals:
            for variable in interval.variables.values():
                if variable.name == "wind_speed":
                    variable.convert_to("km/h")


def sanitize_name(name: str) -> str:
    """Returns a sanitized version of the given name for URLs and file names."""
    return (
        name.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("\\", "")
        .replace("/", "")
    )
