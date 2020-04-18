"""Tests for data containers."""

import datetime as dt
import unittest

from dryrock.forecasts import data_containers


class TestWindVariable(unittest.TestCase):
    """Tests for WindVariable class."""

    def setUp(self):
        self.wind = data_containers.WindVariable(100, "mps", "South")

    def test_convert_100mps_to_kph(self):
        self.wind.convert_mps_to_kph()

        self.assertEqual(self.wind.value, 360)
        self.assertEqual(self.wind.unit, "kph")

    def test_do_not_convert_if_already_kph(self):
        self.wind.unit = "kph"

        self.assertEqual(self.wind.value, 100)
        self.assertEqual(self.wind.unit, "kph")

    def test_raises_error_if_invalid_unit(self):
        self.wind.unit = "not a unit"

        with self.assertRaises(ValueError):
            self.wind.convert_mps_to_kph()


class TestForecast(unittest.TestCase):
    """Tests for Forecast class."""

    def setUp(self):

        rain = data_containers.Variable("Rain", 1.0, "mm")

        day1_interval1 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 1, 0, 1),
            dt.datetime(2020, 1, 1, 1, 0),
            {rain.name: rain},
        )
        day1_interval2 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 1, 1, 1),
            dt.datetime(2020, 1, 1, 2, 0),
            {rain.name: rain},
        )
        day1_interval3 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 1, 2, 1),
            dt.datetime(2020, 1, 1, 3, 0),
            {rain.name: rain},
        )

        day2_interval1 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 2, 0, 1),
            dt.datetime(2020, 1, 2, 1, 0),
            {rain.name: rain},
        )
        day2_interval2 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 2, 1, 1),
            dt.datetime(2020, 1, 2, 2, 0),
            {rain.name: rain},
        )
        day2_interval3 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 2, 2, 1),
            dt.datetime(2020, 1, 2, 3, 0),
            {rain.name: rain},
        )

        day3_interval1 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 3, 0, 1),
            dt.datetime(2020, 1, 3, 1, 0),
            {rain.name: rain},
        )
        day3_interval2 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 3, 1, 1),
            dt.datetime(2020, 1, 3, 2, 0),
            {rain.name: rain},
        )
        day3_interval3 = data_containers.ForecastInterval(
            dt.datetime(2020, 1, 3, 2, 1),
            dt.datetime(2020, 1, 3, 3, 0),
            {rain.name: rain},
        )

        intervals = [
            day1_interval1,
            day1_interval2,
            day1_interval3,
            day2_interval1,
            day2_interval2,
            day2_interval3,
            day3_interval1,
            day3_interval2,
            day3_interval3,
        ]

        self.forecast = data_containers.Forecast(
            "test forecast", None, None, None, intervals
        )

    def test_get_relevant_intervals(self):
        relevant_intervals = self.forecast.get_relevant_intervals(
            dt.date(2020, 1, 1)
        )

        self.assertEqual(len(relevant_intervals), 3)
        self.assertEqual(
            relevant_intervals[0].start_time, dt.datetime(2020, 1, 1, 0, 1)
        )

        relevant_intervals = self.forecast.get_relevant_intervals(
            dt.date(2020, 1, 3)
        )

        self.assertEqual(len(relevant_intervals), 3)
        self.assertEqual(
            relevant_intervals[0].start_time, dt.datetime(2020, 1, 3, 0, 1)
        )
