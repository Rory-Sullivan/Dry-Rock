"""Functions for managing the areas/places we will check."""

import json
from typing import List
from zoneinfo import ZoneInfo

from metno_locationforecast import Place


class Area:
    """Holds data for an area containing multiple places.

    Attributes:
        name: Name of place.
        places: List of places in area.
    """

    def __init__(
        self,
        name: str,
        time_zone: str,
        places: List[Place],
    ):
        """Create an Area object.

        Args:
            name: Name of the place.
            places: List of places in area.
        """
        self.name = name
        self.time_zone = ZoneInfo(time_zone)
        self.places = places

    def __repr__(self) -> str:
        return f"Place({self.name}, {repr(self.places)})"


def get_areas(areas_file: str) -> List[Area]:
    """Returns a list of areas in areas file.

    Raises:
        FileNotFoundError if file does not exist.
    """

    areas: List[Area] = []
    with open(areas_file, "r", encoding="utf8") as file:
        areas_data = json.load(file)

        if not isinstance(areas_data, dict):
            raise ValueError
        if not isinstance(areas_data["areas"], list):
            raise ValueError

        for area in areas_data["areas"]:  # type: ignore
            if not isinstance(area, dict):
                raise ValueError
            if not isinstance(area["area_name"], str):
                raise ValueError
            if not isinstance(area["time_zone"], str):
                raise ValueError
            if not isinstance(area["places"], list):
                raise ValueError

            places: List[Place] = []
            for place in area["places"]:  # type: ignore
                if not isinstance(place, dict):
                    raise ValueError
                if not isinstance(place["place_name"], str):
                    raise ValueError
                if not isinstance(place["latitude"], (float, int)):
                    raise ValueError
                if not isinstance(place["longitude"], (float, int)):
                    raise ValueError
                if not isinstance(place["altitude"], int):
                    raise ValueError

                places.append(
                    Place(
                        place["place_name"],
                        place["latitude"],
                        place["longitude"],
                        place["altitude"],
                    )
                )

            areas.append(Area(area["area_name"], area["time_zone"], places))

    return areas
