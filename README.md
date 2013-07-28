Hard disk drives (HDD) prices over time (1950-present). This dataset provides a
time series of retail prices for "Winchester"-style hard disk drives sourced
from various publications and sources.

## Data

Data in `data.csv` and metadata in `datapackage.json`.

The primary data source was this [great webpage][winchest] (now
sadly offline but available on the Internet Archive). We have a cached copy
(from archive.org) in `archive/winchest-20111107.html`.

[winchest]: http://www.littletechshoppe.com/ns1625/winchest.html

### Processing

The data was extracted using the `process.py` script. Some notes:

* Costs per GB in extracted data do not always accord with those in the
  original webpage. The extracted ones were calculated directly from the price
  and capacity figures rather than using the value in the page. Not sure why
  there is a discrepancy here (sales tax?).
* We have left out the entries corresponding to Note 11 since only cost per MB
  is available.

Running the script:

1. Require python, the datautil and dateutil libraries:

        pip install datautil dateutil

2. Run the python script to:

        python scripts/process.py

### License

Have applied the Open Data Commons Public Domain Dedication and License on basis that:

* Original source data is so small as not to have any copyright or database rights protection
* Maintainers efforts explicitly licensed with PDDL! (And probably also very small!)

Code is licensed under the MIT license.

