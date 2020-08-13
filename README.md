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

- Fork this repo and clone it to your machine
- Install dependencies, ``pip install -r requirements.txt`` (this assumes you
  have Python and Pip installed already), it is probably best to do this in a
  dedicated environment for your app
- Alternatively if you use pipenv you can just run ```pipenv install``` and it
  will install the necessary packages.
- Update the ``./data/input/places.csv`` file, this is where the places you are
  interested in should go
- Run the dryrock module ``python -m dryrock``
- This will create ``index.html`` in your root folder, check it out

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
