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

    def __init__(self, name: str, location: str, yr_link: str):
        self.name = name
        self.location = location
        self.yr_url = f"http://www.yr.no/place/{location}/"
        self.yr_link = yr_link

    def __str__(self):
        return self.name


def create_csv():
    """ Creates places.csv file in input location. """

    if FILE_PATH.exists():
        response = input(
            "places.csv already exists do you wish to overwrite it? (Y/N)"
        ).lower()

        if response == "y":
            with open(FILE_PATH, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["name", "location", "yr_link"])

    else:
        if not INPUT_PATH.exists():
            INPUT_PATH.mkdir(parents=True)

        with open(FILE_PATH, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "location", "yr_link"])


def add_place(place: Place):
    """ Adds a place to places.csv """

    if not FILE_PATH.exists():
        create_csv()

    with FILE_PATH.open("a") as file:
        writer = csv.writer(file)
        writer.writerow([place.name, place.location, place.yr_link])


def get_places():
    """ Returns list of places in places.csv """

    places = []
    with open("./data/input/places.csv", "r") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            place = Place(row["name"], row["location"], row["yr_link"])
            places.append(place)

    return places


def remove_place(name):
    """ Removes a place from places.csv """

    places = get_places()

    for place in places:
        if place.name == name:
            places.remove(place)

    with open(FILE_PATH, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "location", "yr_link"])

        for place in places:
            writer.writerow([place.name, place.location, place.yr_link])
