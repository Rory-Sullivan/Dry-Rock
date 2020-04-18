"""Tests for data containers."""

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
