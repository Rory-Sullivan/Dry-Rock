# Changelog

Here you can find a list of changes to the Dry Rock project as well as up coming
features.

## Unreleased

## [2.0.0] - 2020-08-??

Dry Rock version 2 is here! With the Yr weather API being deprecated later this
year version 2 now uses MET Norway's [weather API](https://api.met.no/). Most
significantly this means that forecast data is exact to each crag rather than
being taken from the nearest town. This change has been aided by using the
[metno-locationforecast](https://github.com/Rory-Sullivan/metno-locationforecast)
library.

There have also been improvements to the general design of the site and the
addition of a more detailed hourly forecast.

### Changed

- Swapped to MET Norway's
  [Locationforecast](https://api.met.no/weatherapi/locationforecast/2.0/documentation)
  service through use of the
  [metno-locationforecast](https://github.com/Rory-Sullivan/metno-locationforecast)
  library
- Forecasts now exact to crags
- First column of tables is now fixed to making viewing easier on small screens

## Added

- Detailed hourly forecasts in pop out modal
- Logging functionality, there is now a logging level configuration in config.py
- About and News pages

## Removed

- The forecast package, as this has been replaced by the
  [metno-locationforecast](https://github.com/Rory-Sullivan/metno-locationforecast)
  library
- Sunrise and sunset times, these are not included in the new API. They may be
  brought back in a future version

## [1.0.0] - 2020-05-25

The initial release of the Dry Rock site.

Dry Rock is a site designed to help climbers in Ireland find some dry rock to
climb on. Weather forecast data is collected from [Yr](https://www.yr.no/en),
provided by the [Norwegian Meteorological Institute](https://www.met.no/en).
