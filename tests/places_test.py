"""Tests for our places functionality."""
import unittest
import os

from dryrock.places import Place, create_csv


class TestPlace(unittest.TestCase):
    """Tests for Place class."""

    def setUp(self):
        self.dublin = Place(
            "Dublin",
            "Ireland/Leinster/Dublin",
            "https://www.yr.no/en/forecast/daily-table/2-2964574",
        )

    def test_attributes(self):
        """Test if attributes are set correctly."""

        value = self.dublin.name
        expected_value = "Dublin"
        self.assertEqual(value, expected_value)

        value = self.dublin.location
        expected_value = "Ireland/Leinster/Dublin"
        self.assertEqual(value, expected_value)

        value = self.dublin.yr_url
        expected_value = "http://www.yr.no/place/Ireland/Leinster/Dublin/"
        self.assertEqual(value, expected_value)

        value = self.dublin.yr_link
        expected_value = "https://www.yr.no/en/forecast/daily-table/2-2964574"
        self.assertEqual(value, expected_value)


class TestPlaces(unittest.TestCase):
    """Tests for creating places.csv, adding getting and removing places."""

    INPUT_PATH = "./tests/input/"
    FILE_PATH = INPUT_PATH.joinpath("places.csv")

    def tearDown(self):
        os.remove(FILE_PATH)
        os.rmdir(INPUT_PATH)

    def test_create_csv(self):
        create_csv()

        self.assertTrue(FILE_PATH.exists())
