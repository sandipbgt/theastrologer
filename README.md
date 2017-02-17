# theastrologer

A Python module to fetch and parse horoscope data from [theastrologer.com](http://theastrologer.com)

## Projects built using theastrologer
* [theastrologer-api](https://github.com/sandipbgt/theastrologer-api) - REST API to view and send horoscope as SMS using theastrologer lilbrary, Flask framework and Twilio API

## Installation
* You will need [Python 3](https://www.python.org/download/).
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

print(today['sunsign'])
print(today['horoscope'])


```

## Features
### Currently implemented
* Today's horoscope
* Yesterday's horoscope
* Tomorrow's horoscope
* List of all horoscope