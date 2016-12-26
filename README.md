# itinerary-finder
The itinerary finder finds potential itineraries given information on such things at train routes, train route times, and stations. The program reads from a database file and outputs to the same database file and a file.
The program is written in Python v3.3 and much be executed with a python interpreter.
After installing [python](https://www.python.org/downloads/), you can run the app like so:
`"C:\python.exe" "C:\itFinder.py"`

## Input
The input file `Trains.mdb` is a database follow with the following tables:
 - STATION_MASTER
 - TRAIN
 - TRAIN_ROUTE
 - PASSENGER_OD_TIME

The program assumes that the input can be read from `C:\Trains.mdb`, but this can be changed by modifying `dataAccess.py`. Please see the sample input file `Trains.mdb` on this github.

## Output
Also included in `Trains.mdb` are a list of tables that are written to when the program runs. The program will delete all existing rows in these tables before outputting to them when executed.
 - ARC
 - NODE
 - TRIP_PLAN

In addition, the itinerary is also output to a file named `tripplan.csv` which contains the same information as the TRIP_PLAN database table.
