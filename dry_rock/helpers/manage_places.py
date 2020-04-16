"""
Functions for managing the places we will check.
"""
import csv
from helpers.general_classes import Place


def create_csv():
    """ Add places to CSV file """

    with open("../data/input/places.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "location", "yr_link"])
        writer.writerow(
            [
                "Dublin",
                "Ireland/Leinster/Dublin",
                "https://www.yr.no/en/forecast/daily-table/2-2964574",
            ]
        )
        writer.writerow(
            [
                "Galway",
                "Ireland/Connacht/Galway",
                "https://www.yr.no/en/forecast/daily-table/2-2964180",
            ]
        )
        writer.writerow(
            [
                "Ballycastle",
                "United_Kingdom/Northern_Ireland/Ballycastle",
                "https://www.yr.no/en/forecast/daily-table/2-2656531",
            ]
        )


def get_places():
    """ Returns list of places in SV file. """

    places = []
    with open("../data/input/places.csv", "r") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            place = Place(row["name"], row["location"], row["yr_link"])
            places.append(place)

    return places


if __name__ == "__main__":
    create_csv()
