# Dry Rock

Dry Rock is a website designed to help climbers in Ireland find some dry rock to
climb on. Check it out at [dryrock.ie](https://dryrock.ie).

The forecast data is sourced from the [Norwegian Meteorological
Institute](https://www.met.no/en).

## Motivations

As a rock climber I am perpetually thinking about my next weekend trip and
trying to decide where looks like the driest place to go. This leads to a lot of
time spent checking forecasts for the various climbing areas in Ireland. As
every programmer knows when a task gets boring and repetitive, you automate it!
So that's what I did.

The site runs a python script at regular intervals. The script retrieves
forecast data from MET Norway's weather API, collates it and renders it into a
single page. This leaves me with a single web page to check before deciding
where to go at the weekend.

## Usage

While I have not designed this project to be used by others you are more than
welcome to, however please see the [licensing notes](#licensing-notes) below.

The gist of how to set up the project is as follows;

- Download the latest release from the [releases
  page](https://github.com/Rory-Sullivan/Dry-Rock/releases) and unpack it into a
  directory
- Install dependencies into a virtual environment
  - If you use pipenv simply run ``pipenv install``
  - If you don't use pipenv you can find a list of dependencies in the
    ``Pipfile``, install these into your environment however you normally would
- Update the ``./data/input/places.csv`` file, this is where the places you are
  interested in should go
- Run the dryrock module ``python -m dryrock``
- This will create an ``index.html`` file in your root folder, check it out
  - Note: for full functionality you will need to serve the file using an http
    server

To access your forecast from anywhere you will need hosting for your site,
personally I use GitHub pages for this. To keep your site up to date consider
running the Python module on a schedule or whenever the page is accessed, I use
GitHub actions. Note that the module will only make a request for data if the
data has expired.

## Licensing notes

While this code is covered by an MIT licence and is free to use, the data
collected from MET Norway is subject to it's own terms of service. Check MET
Norway's website for further details.

- [Meteorological Institute of Norway](https://www.met.no/en)
- [MET Norway API - Terms of Service](https://api.met.no/doc/TermsOfService)
- [MET Norway API - Documentation](https://api.met.no/)
