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

- Fork this repository
- Update the 'setup.cfg' file, particularly the 'user_agent' section under the
  'metno-locationforecast' header
- Update the '/data/input/places.csv/' file with the places that are of interest
  to you
- Setup [GitHub Pages](https://pages.github.com/) for your repository

Hey presto! Your site should be live and will update ever hour using GitHub
workflows.

Also of interest, if you would like to build a similar type of site, is the
[metno-locationforecast](https://github.com/Rory-Sullivan/metno-locationforecast)
library. It makes it super easy for a python application to retrieve data from
the MET Norway API.

## Licensing notes

While this code is covered by an MIT licence and is free to use, the data
collected from MET Norway is subject to it's own terms of service. In particular
they require that any app requesting information from their API identifies
itself correctly and so simply copying this site and requesting data as if you
are this site is a violation of their terms of use. Check MET Norway's website
for further details.

- [Meteorological Institute of Norway](https://www.met.no/en)
- [MET Norway API - Terms of Service](https://api.met.no/doc/TermsOfService)
- [MET Norway API - Documentation](https://api.met.no/)
