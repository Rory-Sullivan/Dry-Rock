"""
Functions for managing the places we will check.
"""
import csv

from dryrock.config import INPUT_PATH

FILE_PATH = INPUT_PATH.joinpath("places.csv")


class Place:
    """
    Stores information for a place.
    """

    def __init__(self, name: str, location: str, yr_link: str, climbing_area=None):
        self.name = name
        self.location = location
        self.yr_url = f"http://www.yr.no/place/{location}/"
        self.yr_link = yr_link

        self.climbing_area = climbing_area if climbing_area else None

    def __str__(self):
        return self.name


def create_file():
    """Creates places.csv file in input location.

    Raises FileExistsError if the file already exists.
    """

    if not INPUT_PATH.exists():
        INPUT_PATH.mkdir(parents=True)

    with open(FILE_PATH, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "climbing_area" "location", "yr_link"])


def get_places():
    """Returns list of places in places file.

    Raises FileNotFoundError if file does not exist.
    """

    places = []
    with open(FILE_PATH, "r") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            place = Place(row["name"], row["location"], row["yr_link"], row["climbing_area"])
            places.append(place)

    return places
