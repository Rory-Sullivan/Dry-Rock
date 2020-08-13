"""Functions for managing the places we will check."""

import csv
from typing import List

from metno_locationforecast import Place


def get_places(places_file: str) -> List[Place]:
    """Returns list of places in places file.

    Raises:
        FileNotFoundError if file does not exist.
    """

    places = []
    with open(places_file, "r") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            place = Place(
                row["name"], float(row["latitude"]), float(row["longitude"]), int(row["altitude"])
            )
            places.append(place)

    return places
