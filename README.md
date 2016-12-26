# itinerary-finder
An itinerary finder that loads data from a Microsoft Access mdb file and outputs an itinerary to to a file named `tripplan.csv` and to database tables ARC, NODE, and TRIP_PLAN.
The program assumes that the input can be read from `C:\Trains.mdb`, but this can be changed by modifying `dataAccess.py`. Please see the sample input file `Trains.mdb` on this github.
The program is written in Python v3.3 and much be executed with a python interpreter.
After installing [python](https://www.python.org/downloads/), you can run the app like so:
`"C:\python.exe" "C:\itFinder.py"`

## Getting Started
The input file `Trains.mdb` is a database follow with the following tables:
 - STATION_MASTER
 - TRAIN
 - TRAIN_ROUTE
 - PASSENGER_OD_TIME

Also included in `Trains.mdb` are a list of tables that are written to when the program runs. The program will delete all existing rows in these tables before outputting to them when executed.
 - ARC
 - NODE
 - TRIP_PLAN
