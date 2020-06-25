# Dry-Rock

Dry Rock is a site designed to help climbers in Ireland find some dry rock to
climb on. Check it out [here](https://rory-sullivan.github.io/Dry-Rock/).

The forecasting data is sourced from [Yr](https://www.yr.no/en), delivered by the
[Norwegian Meteorological Institute](https://www.met.no/en) and
[NRK](https://www.nrk.no/).

## Motivations

As a rock climber I am perpetually thinking about my next weekend trip and
trying to decide where looks like the driest place to go. This leads to a lot of
time spent checking forecasts for the various climbing areas in Ireland. As
every programmer knows when a task gets boring and repetitive, you automate it!
So that's what I did.

The site runs a python script at regular intervals. The script retrieves
forecast data from Yr, collates it and renders it into a single page. This
leaves me with a single web page to check before deciding where to go at the
weekend.

## Usage

While I have not designed this project to be used by others you are more than
welcome to, however please see the [licensing notes](#licensing-notes) below.

The gist of how to set up the project is as follows;

- Clone the repo to your desired location
- Install dependencies ``pip install -r requirements.txt`` (this assumes you
  have Python and Pip installed already)
- Update the ``./data/input/places.csv`` file, this is where the places you are
  interested in should go
- Run the dryrock module ``python -m dryrock``
- This will create ``index.html`` in your root folder, check it out

To access your forecast from anywhere you will need hosting for your site,
personally I use GitHub pages for this. To keep your site up to date consider
running the Python module on a schedule or whenever the page is accessed, I use
GitHub actions. Note that the module will only pull data from Yr if the data has
been updated since the last pull.

## Licensing notes

While this code is covered by an MIT licence and is free to use the data
collected from Yr is subject to it's own terms of use. Check the Yr website for
further details.

- <https://hjelp.yr.no/hc/en-us/articles/360001946134-Data-access-and-terms-of-service>
- <https://hjelp.yr.no/hc/en-us/categories/200450271-About-Yr-the-API-and-our-privacy-policy>
