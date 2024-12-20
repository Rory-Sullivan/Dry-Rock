import copy
import datetime as dt
from enum import Enum
from typing import List, Tuple

from metno_locationforecast.data_containers import Interval, Variable


class UnitSystem(Enum):
    METRIC = 0
    IMPERIAL = 1


class ColourVariant(Enum):
    GOOD = "success"
    OKAY = "warning"
    BAD = "danger"


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


def change_units(variable: Variable, unit_system: UnitSystem) -> Variable:
    """Returns a new instance of the variable in the given unit system"""

    variable = copy.deepcopy(variable)
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
    return variable


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


def get_time_delta(start_time: dt.time, end_time: dt.time) -> dt.timedelta:
    """
    Returns the time delta in hours between two times, rounding to the nearest
    hour.

    If start_time is later than end_time assumes that end_time falls in the next
    day.
    """

    if start_time.hour > end_time.hour or (
        start_time.hour == end_time.hour and start_time.minute > end_time.minute
    ):
        hours = (24 - start_time.hour) + end_time.hour
    else:
        hours = end_time.hour - start_time.hour

    if end_time.minute - start_time.minute >= 30:
        hours += 1
    if end_time.minute - start_time.minute < -30:
        hours -= 1

    return dt.timedelta(hours=hours)


def get_time_delta_hours(time_delta: dt.timedelta) -> float:
    return abs(time_delta.total_seconds() / 3600)


def _get_precipitation_colour_variant(variable: Variable, time_delta: dt.timedelta) -> str:
    PRECIPITATION_OKAY_PER_HOUR = 0.5  # millimetres
    PRECIPITATION_BAD_PER_HOUR = 2.0  # millimetres

    if variable.name != "precipitation_amount":
        raise ValueError(
            f"Can only be called with 'precipitation_amount' variable, given variable: {variable.name}"  # noqa E501
        )
    if variable.units != "mm":
        raise ValueError(
            f"Can only be called with units set to mm, given units: {variable.units}"  # noqa E501
        )

    time_delta_hours = get_time_delta_hours(time_delta)
    bad_value = PRECIPITATION_BAD_PER_HOUR * time_delta_hours
    okay_value = PRECIPITATION_OKAY_PER_HOUR * time_delta_hours

    if bad_value and variable.value >= bad_value:
        return ColourVariant.BAD.value

    if okay_value and variable.value >= okay_value:
        return ColourVariant.OKAY.value

    return ColourVariant.GOOD.value


def get_colour_variant(variable: Variable, time_delta: dt.timedelta | None = None) -> str:
    if variable.name == "precipitation_amount":
        if time_delta is None:
            raise ValueError("time_delta cannot be none for precipitation type variable")
        return _get_precipitation_colour_variant(variable, time_delta)

    raise ValueError(f"Cannot get colour variant for variable type: {variable.name}")
