>**Note**: This work was done as part of the Udacity Nanodegree programm **Programming for Data Science with Python**.

### Date created
12:24 Dienstag, 25. Februar 2025

# US Bikeshare Data Project

## Description
This is a simple interactive Python script to explore data related to bike share systems for three major cities in the United States
- Chicago, 
- New York City, and 
- Washington.

It allows the user to select the city and date filters.
Once data and date filters are selected, the user can decide between 3 options:
- display basic dataset infos,
- browse the raw data or
- execute the data exploration.

### The Datasets
The data files are based on data available at [Divvy Bikes](https://divvybikes.com/system-data).
It has gone through some data wrangling by Udacity.
Randomly selected data for the first six months of 2017 are provided for all three cities. All three of the data files contain the same core six (6) columns:

- Start Time (e.g., 2017-01-01 00:07:57)
- End Time (e.g., 2017-01-01 00:20:53)
- Trip Duration (in seconds - e.g., 776)
- Start Station (e.g., Broadway & Barry Ave)
- End Station (e.g., Sedgwick St & North Ave)
- User Type (Subscriber or Customer)

The Chicago and New York City files also have the following two columns:
- Gender
- Birth Year

_Italic_

**BOLD**

## Files used
The script is named
`bikeshare_zj_v3.py`

and has to be run locally from the command line.

In it's current version, it accepts no command line arguments.
The data for the 3 cities has to be made available in csv files named
- `chicago.csv`
- `washington.csv`
- `new_york_city.csv`

These files have to available in the directory where the Python file is loated.


### Credits
This repo is based on the following [Udacity repo](https://github.com/udacity/pdsnd_github).


