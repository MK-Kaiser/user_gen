## Purpose

This was created as the limitations of username alchamy started to fail me. I do like that username-alchamy allows for varying countries, but I can work on that later.

## Usage
```python
usage: usernames.py [-h] [-f str] [-tf n] [-ts n] [-c n] [-y n] [-t type] [-s]
                    [-d] [-v] [-uo | -o filename]

Generates a list of usernames from SSA and Namecensus respositories.

optional arguments:
  -h, --help            show this help message and exit
  -f str, --format str  This sets the format for username output. Choices are:
                        first.last, f.last, first.l, flast, firstl, firstlast,
                        first, last.
  -tf n, --top-firstnames n
                        This is the top number of firstnames to return from
                        the SSA query for each year specified. The min
                        selection is 1 and the max is 1000. Any value less
                        then 1 will result in a value of 10 being returned.
                        This is not the total amount of useranmes returned, as
                        they will be combined with surnames. This feature is
                        meant to be used in conjunction with the -f first only
                        specification. Additonally, this number is doubled if
                        "combined" is selected from the type. Default: 1000
  -ts n, --top-surnames n
                        This is the top number of surnames to return from the
                        name census query. The min selection is 1. This is not
                        the total amount of useranmes returned. Default: 1000
  -c n, --count n       This returns only n number of usernames. Default: 0
                        (all)
  -y n, --years n       This is the number of previous years to search
                        starting from the current year. This will increase
                        your firstname results. Default: 2
  -t type, --type type  This is the type of firstnames to return. Choices are:
                        male, female, combined. Default: combined
  -s, --sort            This sorts the final list of usernames alphabetically.
                        Default: False
  -d, --debug           This prints the output from the web requets. Default:
                        False
  -v, --verbosity       This does nolthing at the moment. Default: False
  -uo, --usernames-only
                        This only outputs the usernames and none of the filler
                        text. This can be used when piping this into another
                        command. This will disable verbosity if enabled.
                        Default: False
  -o str, --output str
                        This is the filename of the output file. The file will
                        be created in the /tmp/ directory and not print to
                        stdout. Cannot be used in conjunction with the -uo
                        flag. Default: stdout.
```

## Examples
### Limiting the username count
```python
python3 ./usernames.py -f first.last -y 3 -c 10

Unable to find data for year of birth 2020
There seems to be no results for year 2019
Results discvoered for birth year of 2018
Gathering surnames.
Completed gathering surnames
################################
addilynn.quinn
michael.frazier
fernanda.wilkerson
nicholas.meyer
jonathan.ward
yahir.berry
josie.sullivan
jordyn.hoffman
eduardo.parsons
musa.garza
```

### Anything over 2000 makes sure your buffer is ready to handle it
```python
python3 ./usernames.py -f first.last -y 3        
Unable to find data for year of birth 2020
There seems to be no results for year 2019
Results discvoered for birth year of 2018
Gathering surnames.
Completed gathering surnames

The result of this are over 2000 possibilities (1,922,000 total)
Would you prefer to save these as a file? [Y/n]: n
Ok, printing to stdout then. Hope you have time and your line buffer is set correctly...
################################
devin.richard
penelope.holder
andi.stone
adelyn.snow
carly.mack
maliyah.kent
roman.heath
```

### Piping output to other script
```python
python3 ./usernames.py -f first.last -y 3 -uo | xargs -I {} echo "//something awesome "{}
//something awesome walker.cunningham
//something awesome aria.page
//something awesome eddie.miles
//something awesome elizabeth.chapman
//something awesome jayson.elliott
//something awesome mordechai.compton
//something awesome chana.sharpe
//something awesome sincere.hayes
//something awesome joy.mclean
//something awesome zechariah.cruz
```
