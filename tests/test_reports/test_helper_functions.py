import datetime as dt
from typing import List

import pytest
from metno_locationforecast import Forecast, Place
from metno_locationforecast.data_containers import Interval, Variable

from dryrock.reports.helper_functions import (
    cardinal_name_of,
    max_temp_of,
    max_wind_speed_of,
    min_temp_of,
    sanitize_name,
    sum_rain,
)


@pytest.fixture
def dalkey_intervals_for_day():
    dalkey = Place("Dalkey Quarry", 53.271, -6.107, 95)
    d_forecast = Forecast(dalkey, save_location="./tests/test_data/")
    d_forecast.load()
    day = dt.date(2020, 8, 7)

    return d_forecast.data.intervals_for(day)


def test_cardinal_name_of():
    north = Variable("wind_from_direction", 0, "degrees")
    east = Variable("wind_from_direction", 100, "degrees")
    southwest = Variable("wind_from_direction", 203, "degrees")
    northwest = Variable("wind_from_direction", 337, "degrees")
    not_real = Variable("wind_from_direction", -1, "degrees")

    assert cardinal_name_of(north) == "North"
    assert cardinal_name_of(east) == "East"
    assert cardinal_name_of(southwest) == "Southwest"
    assert cardinal_name_of(northwest) == "Northwest"
    with pytest.raises(RuntimeError):
        cardinal_name_of(not_real)


def test_sum_rain(dalkey_intervals_for_day: List[Interval]):
    expected = Variable(
        "precipitation_amount", 0.30000000000000004, "mm"
    )  # Crazy number due to floating point limitations in python.

    assert sum_rain(dalkey_intervals_for_day) == expected


def test_max_temp_of(dalkey_intervals_for_day: List[Interval]):
    expected = Variable("air_temperature", 21.0, "celsius")

    assert max_temp_of(dalkey_intervals_for_day) == expected


def test_min_temp_of(dalkey_intervals_for_day: List[Interval]):
    expected = Variable("air_temperature", 14.6, "celsius")

    assert min_temp_of(dalkey_intervals_for_day) == expected


def test_max_wind_speed_of(dalkey_intervals_for_day: List[Interval]):
    expected = (
        Variable("wind_speed", 5.1, "m/s"),
        Variable("wind_from_direction", 183.3, "degrees"),
    )

    assert max_wind_speed_of(dalkey_intervals_for_day) == expected


def test_sanitize_name():
    name_1 = "easy"
    expected_1 = "easy"
    assert sanitize_name(name_1) == expected_1

    name_2 = "with space"
    expected_2 = "with_space"
    assert sanitize_name(name_2) == expected_2

    name_3 = "With CAPS"
    expected_3 = "with_caps"
    assert sanitize_name(name_3) == expected_3

    name_4 = "with (brackets)"
    expected_4 = "with_brackets"
    assert sanitize_name(name_4) == expected_4

    name_5 = "with /slashes\\"
    expected_5 = "with_slashes"
    assert sanitize_name(name_5) == expected_5
