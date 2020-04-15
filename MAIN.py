"""
Collects weather data from websites for various locations, collates the data and emails a report to a list of users.
"""
# Import project files.
from general_classes import Place
from weather_data import WeatherData
from manage_places import get_places
from email_stuff import get_addresses, send_email

# Import libraries.
import datetime as dt


# Get a time for this run.
now = dt.datetime.now()
print(f"Collecting weather data at {now}")

# Get places we are going to check.
if __name__ == "__main__":
    places = get_places()
# For testing purposes we will just use Dublin.
else:
    places = [
        Place(
            "Dublin",
            "Ireland/Leinster/Dublin",
            "https://www.yr.no/en/forecast/daily-table/2-2964574",
        )
    ]

# Get data.
current_data = WeatherData(now, places)

#  Update text report.
current_data.update_text_report()


# Update the html report.
current_data.update_html_report()


# We will not send an email if we are testing the code.
if __name__ == "__main__":
    addresses = get_addresses()
    send_email(addresses)
