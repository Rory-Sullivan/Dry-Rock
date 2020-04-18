"""Tests for our places functionality."""
import unittest
import os
import pathlib

from dryrock import places


class TestPlace(unittest.TestCase):
    """Tests for Place class."""

    def setUp(self):
        self.dublin = places.Place(
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


class TestCreateFile(unittest.TestCase):
    """Tests for creating places.csv."""

    @classmethod
    def setUpClass(cls):
        places.INPUT_PATH = pathlib.Path("./tests/input/")
        places.FILE_PATH = places.INPUT_PATH.joinpath("places.csv")

    def tearDown(self):
        if places.FILE_PATH.exists():
            os.remove(places.FILE_PATH)

        if places.INPUT_PATH.exists():
            os.rmdir(places.INPUT_PATH)

    def test_create_csv(self):
        places.create_file()

        self.assertTrue(places.FILE_PATH.exists())


class TestGetPlaces(unittest.TestCase):
    """Tests for get_places() function."""

    @classmethod
    def setUpClass(cls):
        places.INPUT_PATH = pathlib.Path("./tests/fixtures/")

    def test_simple_case(self):
        places.FILE_PATH = places.INPUT_PATH.joinpath("simple_places.csv")

        simple_places = places.get_places()

        self.assertIsInstance(simple_places, list)
        self.assertEqual(len(simple_places), 3)
        self.assertEqual(simple_places[0].name, "Dublin")


if __name__ == "__main__":
    unittest.main()
