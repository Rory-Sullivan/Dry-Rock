"""Tests for our places functionality."""

import pytest
from metno_locationforecast import Place

from dryrock import places


@pytest.fixture
def simple_areas_file():
    return "./tests/test_data/simple_areas.json"


class TestGetPlaces:
    def test_with_simple_places_file(self, simple_areas_file: str):
        areas = places.get_areas(simple_areas_file)

        assert len(areas) == 2

        assert areas[0].name == "Ireland"
        expected_places_1 = [
            Place("Dalkey Quarry", 53.271, -6.107, 100),
            Place("Glendalough", 53.009, -6.387, 450),
            Place("Fair Head", 55.225, -6.154, 150),
        ]
        assert len(areas[0].places) == len(expected_places_1)
        for i in range(len(expected_places_1)):
            assert repr(areas[0].places[i]) == repr(expected_places_1[i])

        assert areas[1].name == "Washington"
        expected_places_1 = [
            Place("I90 Exit 32", 47.49795, -121.75474, 367),
        ]
        assert len(areas[1].places) == len(expected_places_1)
        for i in range(len(expected_places_1)):
            assert repr(areas[1].places[i]) == repr(expected_places_1[i])

    def test_with_non_existent_file(self):
        with pytest.raises(FileNotFoundError):
            places.get_areas("Not a file")
