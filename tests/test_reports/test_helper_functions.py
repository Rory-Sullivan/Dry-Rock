import datetime as dt
from typing import List

import pytest
from metno_locationforecast import Forecast, Place
from metno_locationforecast.data_containers import Interval, Variable

from dryrock.reports.helper_functions import (
    ColourVariant,
    cardinal_name_of,
    _get_precipitation_colour_variant,  # type: ignore (use of private function outside of module)
    get_time_delta,
    get_time_delta_hours,
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


def test_get_time_delta():
    # 0 hours
    assert get_time_delta(start_time=dt.time(hour=1), end_time=dt.time(hour=1)) == dt.timedelta(
        hours=0
    )

    # 1 hour
    assert get_time_delta(start_time=dt.time(hour=1), end_time=dt.time(hour=2)) == dt.timedelta(
        hours=1
    )

    # 6 hours
    assert get_time_delta(start_time=dt.time(hour=12), end_time=dt.time(hour=18)) == dt.timedelta(
        hours=6
    )

    # 24 hours, with rounding
    assert get_time_delta(
        start_time=dt.time(hour=0), end_time=dt.time(hour=23, minute=59)
    ) == dt.timedelta(hours=24)

    # Round up
    assert get_time_delta(
        start_time=dt.time(hour=1), end_time=dt.time(hour=1, minute=30)
    ) == dt.timedelta(hours=1)

    # Round down
    assert get_time_delta(
        start_time=dt.time(hour=1), end_time=dt.time(hour=1, minute=29)
    ) == dt.timedelta(hours=0)

    # Round up, negative
    assert get_time_delta(
        start_time=dt.time(hour=1, minute=45), end_time=dt.time(hour=2, minute=15)
    ) == dt.timedelta(hours=1)

    # Round down, negative
    assert get_time_delta(
        start_time=dt.time(hour=1, minute=45), end_time=dt.time(hour=2, minute=14)
    ) == dt.timedelta(hours=0)

    # If start_time is greater than end_time then assume that end_time falls in
    # the next day.
    assert get_time_delta(start_time=dt.time(hour=23), end_time=dt.time(hour=5)) == dt.timedelta(
        hours=6
    )
    assert get_time_delta(
        start_time=dt.time(hour=0, minute=45), end_time=dt.time(hour=0, minute=14)
    ) == dt.timedelta(hours=23)


def test_get_time_delta_hours():
    # 1 day
    assert (
        get_time_delta_hours(
            dt.datetime(year=2024, month=12, day=7, hour=0)
            - dt.datetime(year=2024, month=12, day=6, hour=0)
        )
        == 24.0
    )

    # 1 day backwards
    assert (
        get_time_delta_hours(
            dt.datetime(year=2024, month=12, day=6, hour=0)
            - dt.datetime(year=2024, month=12, day=7, hour=0)
        )
        == 24.0
    )

    # 6 hours
    assert (
        get_time_delta_hours(
            dt.datetime(year=2024, month=12, day=6, hour=18)
            - dt.datetime(year=2024, month=12, day=6, hour=12)
        )
        == 6.0
    )

    # 1 hours
    assert (
        get_time_delta_hours(
            dt.datetime(year=2024, month=12, day=6, hour=13)
            - dt.datetime(year=2024, month=12, day=6, hour=12)
        )
        == 1.0
    )

    # 2.5 hours
    assert (
        get_time_delta_hours(
            dt.datetime(year=2024, month=12, day=6, hour=14, minute=30)
            - dt.datetime(year=2024, month=12, day=6, hour=12)
        )
        == 2.5
    )


def test_get_precipitation_colour_variant():
    OKAY_VALUE = 0.5
    BAD_VALUE = 2.0

    # 1 hour, good
    one_hour = dt.timedelta(hours=1)
    var = Variable("precipitation_amount", 0.0, "mm")
    assert _get_precipitation_colour_variant(var, one_hour) == ColourVariant.GOOD.value
    var.value = OKAY_VALUE - 0.1
    assert _get_precipitation_colour_variant(var, one_hour) == ColourVariant.GOOD.value

    # 1 hour, metric, okay
    var.value = OKAY_VALUE
    assert _get_precipitation_colour_variant(var, one_hour) == ColourVariant.OKAY.value
    var.value = BAD_VALUE - 0.1
    assert _get_precipitation_colour_variant(var, one_hour) == ColourVariant.OKAY.value

    # 1 hour, metric, bad
    var.value = BAD_VALUE
    assert _get_precipitation_colour_variant(var, one_hour) == ColourVariant.BAD.value

    # 2 hour, metric, good
    two_hour = dt.timedelta(hours=2)
    var.value = 0.0
    assert _get_precipitation_colour_variant(var, two_hour) == ColourVariant.GOOD.value
    var.value = (OKAY_VALUE - 0.1) * 2
    assert _get_precipitation_colour_variant(var, two_hour) == ColourVariant.GOOD.value

    # 2 hour, metric, okay
    var.value = OKAY_VALUE * 2
    assert _get_precipitation_colour_variant(var, two_hour) == ColourVariant.OKAY.value
    var.value = (BAD_VALUE - 0.1) * 2
    assert _get_precipitation_colour_variant(var, two_hour) == ColourVariant.OKAY.value

    # 2 hour, metric, bad
    var.value = BAD_VALUE * 2
    assert _get_precipitation_colour_variant(var, two_hour) == ColourVariant.BAD.value

    # 1 day, metric, good
    one_day = dt.timedelta(days=1)
    var.value = 0.0
    assert _get_precipitation_colour_variant(var, one_day) == ColourVariant.GOOD.value
    var.value = (OKAY_VALUE - 0.1) * 24
    assert _get_precipitation_colour_variant(var, one_day) == ColourVariant.GOOD.value

    # 1 day, metric, okay
    var.value = OKAY_VALUE * 24
    assert _get_precipitation_colour_variant(var, one_day) == ColourVariant.OKAY.value
    var.value = (BAD_VALUE - 0.1) * 24
    assert _get_precipitation_colour_variant(var, one_day) == ColourVariant.OKAY.value

    # 1 day, metric, bad
    var.value = BAD_VALUE * 24
    assert _get_precipitation_colour_variant(var, one_day) == ColourVariant.BAD.value

    # Raises value error when given incorrect units
    with pytest.raises(ValueError):
        var = Variable("precipitation_amount", 0.0, "inches")
        _get_precipitation_colour_variant(var, one_hour)

    # Raises value error when given incorrect variable type
    with pytest.raises(ValueError):
        var = Variable("temperature", 0.0, "celsius")
        _get_precipitation_colour_variant(var, one_hour)
