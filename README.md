# theastrologer

A Python module to fetch and parse horoscope data from [theastrologer.com](http://theastrologer.com)

## Installation
* You will need [Python 4](https://www.python.org/download/).
* [pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

## Installing dependencies
```sh
pip install requests lxml six
```
## Installing theastrologer library:
```sh
pip install theastrologer
```

## Usage
```python

from theastrologer import Horoscope

horoscope = Horoscope("aquarius")
today = horoscope.today()

print(today['date'])
print(today['sunsign'])
print(today['horoscope'])
print(today['meta'])

```

## Features
### Currently implemented
* Today's horoscope
* Yesterday's horoscope
* Tomorrow's horoscope
