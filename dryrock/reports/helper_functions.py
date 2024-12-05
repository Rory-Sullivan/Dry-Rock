from enum import Enum
from typing import List, Tuple

from metno_locationforecast import Forecast
from metno_locationforecast.data_containers import Interval, Variable


class UnitSystem(Enum):
    METRIC = 0
    IMPERIAL = 1


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
    if len(intervals) == 0:
        raise ValueError("Intervals cannot be empty.")

    total_rain = intervals[0].variables["precipitation_amount"]
    for interval in intervals[1:]:
        total_rain += interval.variables["precipitation_amount"]
    return total_rain


def max_temp_of(intervals: List[Interval]) -> Variable:
    if len(intervals) == 0:
        raise ValueError("Intervals cannot be empty.")

    max_temp = intervals[0].variables["air_temperature"]
    for interval in intervals[1:]:
        if max_temp.value < interval.variables["air_temperature"].value:
            max_temp = interval.variables["air_temperature"]
    return max_temp


def min_temp_of(intervals: List[Interval]) -> Variable:
    if len(intervals) == 0:
        raise ValueError("Intervals cannot be empty.")

    min_temp = intervals[0].variables["air_temperature"]
    for interval in intervals[1:]:
        if min_temp.value > interval.variables["air_temperature"].value:
            min_temp = interval.variables["air_temperature"]
    return min_temp


def max_wind_speed_of(intervals: List[Interval]) -> Tuple[Variable, Variable]:
    if len(intervals) == 0:
        raise ValueError("Intervals cannot be empty.")

    max_wind_speed = intervals[0].variables["wind_speed"]
    max_wind_speed_direction = intervals[0].variables["wind_from_direction"]
    for interval in intervals[1:]:
        if max_wind_speed.value < interval.variables["wind_speed"].value:
            max_wind_speed = interval.variables["wind_speed"]
            max_wind_speed_direction = interval.variables["wind_from_direction"]
    return max_wind_speed, max_wind_speed_direction


def change_units(forecasts: List[Forecast], unit_system: UnitSystem) -> None:
    """Change all units of forecast to the given unit system"""

    for forecast in forecasts:
        for interval in forecast.data.intervals:
            for variable in interval.variables.values():
                if variable.name == "precipitation_amount":
                    match unit_system:
                        case UnitSystem.METRIC:
                            variable.convert_to("mm")
                        case UnitSystem.IMPERIAL:
                            variable.convert_to("inches")
                if variable.name == "air_temperature":
                    match unit_system:
                        case UnitSystem.METRIC:
                            variable.convert_to("celsius")
                        case UnitSystem.IMPERIAL:
                            variable.convert_to("fahrenheit")
                if variable.name == "wind_speed":
                    match unit_system:
                        case UnitSystem.METRIC:
                            variable.convert_to("km/h")
                        case UnitSystem.IMPERIAL:
                            variable.convert_to("mph")


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
