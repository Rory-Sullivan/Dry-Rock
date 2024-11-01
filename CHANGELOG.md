# Changelog

Here you can find a list of changes to the Dry Rock project as well as upcoming
features.

## [2.1.1] - 2024-11-01

### Fixed

- Bug causing daily detailed modals to break Lower Cove location

## [2.1.0] - 2024-11-01

### Added

- New locations to forecast; Lower Cove, Cruit Island, and Garron Point

### Changed

- Updated dependencies to newer versions

## [2.0.2] - 2020-08-28

### Added

- A test workflow to automatically lint and test files on pushes and
  pull-requests to master and dev branches
- A deploy workflow which automatically merges the main branch into the gh-pages
  branch and updates the site, on pushes to the main branch
- An update-site action which runs the dryrock module and updates the live site

### Changed

- Updated metno-locationforecast requirement to v1.0.0
- Renamed default branch to 'main'

### Removed

- "requirements.txt" file. The project will now rely on the "Pipfile.lock"

## [2.0.1] - 2020-08-17

Patch v2.0.1

### Fixed

- Typos and wording
- "Updated at" dates now in dd/mm/yyyy format

## [2.0.0] - 2020-08-14

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

### Added

- Detailed hourly forecasts in pop out modal
- Logging functionality, there is now a logging level configuration in config.py
- About and News pages
- Navbar at top of all pages

### Removed

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
