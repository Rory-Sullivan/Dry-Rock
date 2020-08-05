"""Tests for our places functionality."""

import pytest
from metno_locationforecast import Place

from dryrock import places


@pytest.fixture
def simple_places_file():
    return "./tests/test_data/simple_places.csv"


class TestGetPlaces:
    def test_with_simple_places_file(self, simple_places_file):
        expected = [
            Place("Dalkey Quarry", 53.271, -6.107, 100),
            Place("Glendalough", 53.009, -6.387, 450),
            Place("Fair Head", 55.225, -6.154, 150),
        ]
        received = places.get_places(simple_places_file)

        assert len(expected) == len(received)
        for i in range(len(expected)):
            assert repr(expected[i]) == repr(received[i])

    def test_with_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            places.get_places("Not a file")
