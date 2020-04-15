"""
Functions for managing the places we will check.
"""
import csv
from general_classes import Place


def create_csv():
    with open('places.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "location", "yr_link"])
        writer.writerow(["Dublin", "Ireland/Leinster/Dublin",
                         "https://www.yr.no/en/forecast/daily-table/2-2964574"])
        writer.writerow(["Galway", "Ireland/Connacht/Galway",
                         "https://www.yr.no/en/forecast/daily-table/2-2964180"])
        writer.writerow(["Ballycastle", "United_Kingdom/Northern_Ireland/Ballycastle",
                         "https://www.yr.no/en/forecast/daily-table/2-2656531"])


def get_places():
    places = []
    with open("places.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            place = Place(row["name"], row["location"], row["yr_link"])
            places.append(place)

    return places


if __name__ == "__main__":
    create_csv()
    # places = get_places()
    # for place in places:
    #     print(f"{place.name} {place.yr_link}")
