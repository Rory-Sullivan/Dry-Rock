from datetime import datetime
import pytest
from metno_locationforecast import Place, Forecast
from metno_locationforecast.data_containers import Variable
import datetime as dt
from dryrock.reports.helper_functions import (
    cardinal_name_of,
    sum_rain,
    max_temp_of,
    min_temp_of,
    max_wind_speed_of,
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


def test_sum_rain(dalkey_intervals_for_day):
    expected = Variable(
        "precipitation_amount", 0.30000000000000004, "mm"
    )  # Crazy number due to floating point limitations in python.

    assert sum_rain(dalkey_intervals_for_day) == expected


def test_max_temp_of(dalkey_intervals_for_day):
    expected = Variable("air_temperature", 21.0, "celsius")

    assert max_temp_of(dalkey_intervals_for_day) == expected


def test_min_temp_of(dalkey_intervals_for_day):
    expected = Variable("air_temperature", 14.6, "celsius")

    assert min_temp_of(dalkey_intervals_for_day) == expected


def test_max_wind_speed_of(dalkey_intervals_for_day):
    expected = (
        Variable("wind_speed", 5.1, "m/s"),
        Variable("wind_from_direction", 183.3, "degrees"),
    )

    assert max_wind_speed_of(dalkey_intervals_for_day) == expected
