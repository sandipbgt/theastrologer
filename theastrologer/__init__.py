# -*- coding: utf-8 -*-
"""
    theastrologer
    ~~~~~~~~~~~~~

    theastrologer module
"""

from datetime import date, timedelta
from requests import get
from requests.exceptions import RequestException, Timeout
from lxml import html
from six import u
import json

__version__ = '0.1.5'

def is_valid_horoscope_type(horoscope_type):
    horoscope_types = ['daily']
    if horoscope_type not in horoscope_types:
        return False
    return True

def is_valid_day(day):
    days = ['today', 'yesterday', 'tomorrow']
    if day not in days:
        return False
    return True

def is_valid_sunsign(sunsign):
    sunsigns = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    if sunsign not in sunsigns:
        return False
    return True

def build_horoscope_url(base_url, horoscope_type):
    url = ''
    if horoscope_type == 'daily':
        url = base_url + '/daily-horoscope/'
    return url

def scrape_horoscopes_as_dict(tree, day):
    divs = tree.xpath('//*[@id="' + day + '"]/div[4]/div')
    horoscopes = {}
    for div in divs:
        sunsign = div.xpath('h2/text()')[0].strip()
        horoscope = div.xpath('string()').replace(sunsign + '\n', '').replace('\n', '').strip()
        horoscopes[sunsign.lower()] = horoscope
    return horoscopes

def scrape_horoscopes_as_list(tree, day):
    divs = tree.xpath('//*[@id="' + day + '"]/div[4]/div')
    horoscopes = []
    for div in divs:
        horoscope = {}
        horoscope['sunsign'] = div.xpath('h2/text()')[0].strip()
        horoscope['horoscope'] = div.xpath('string()').replace(horoscope['sunsign'] + '\n', '').replace('\n', '').strip()
        horoscopes.append(horoscope)
    return horoscopes


class HoroscopeException(Exception):
    """Horoscope exception
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        """ Try to pretty-print the exception, if this is going on screen. """

        def red(words):
            return u("\033[31m\033[49m%s\033[0m") % words

        def blue(words):
            return u("\033[34m\033[49m%s\033[0m") % words

        msg = (
                "\n{red_error}"
                "\n\n{message}\n".format(
                    red_error=red("Error occured"),
                    message=blue(str(self.msg))
                ))
        return msg

class Horoscope(object):

    def __init__(self, sunsign='aries', horoscope_type='daily'):
        """
        Create a Horoscope
        """

        if not is_valid_horoscope_type(horoscope_type):
            raise HoroscopeException("Invalid horoscope type. Allowed horososcpe types: [daily]" )

        if not is_valid_sunsign(sunsign):
            raise HoroscopeException("Invalid horoscope sunsign")

        self.base_url = "http://new.theastrologer.com"        
        self.sunsign = sunsign.lower()
        self.horoscope_type = horoscope_type.lower()
        self.url = build_horoscope_url(self.base_url, self.horoscope_type)

        self.date_today = date.today()
        
        try:
            self.html_resp = get(self.url)
        except Timeout as e:
            raise HoroscopeException(e)
        except RequestException as e:
            raise HoroscopeException(e)

        self.tree = html.fromstring(self.html_resp.content)

    def _get_horoscope(self, day='today'):
        """gets a horoscope from site html

        :param day: day for which to get horoscope. Default is 'today'

        :returns: dictionary of horoscope details
        """

        if not is_valid_day(day):
            raise HoroscopeException("Invalid day. Allowed days: [today|yesterday|tomorrow]" )

        horoscope = scrape_horoscopes_as_dict(self.tree, day)[self.sunsign]

        return {
            'sunsign': self.sunsign.capitalize(),
            'horoscope': horoscope + " (c) Kelli Fox, The Astrologer, http://new.theastrologer.com",
            'credit': '(c) Kelli Fox, The Astrologer, http://new.theastrologer.com'
        }

    def yesterday(self):
        """gets yesterday's horoscope

        :returns: dictionary of horoscope details
        """
        return self._get_horoscope('yesterday')

    def today(self):
        """gets today's horoscope

        :returns: dictionary of horoscope details
        """
        return self._get_horoscope('today')

    def tomorrow(self):
        """gets tomorrow's horoscope

        :returns: dictionary of horoscope details
        """
        return self._get_horoscope('tomorrow')

    def all(self, day):
        """gets all horoscope as dict

        :returns: dictionary of all horoscope
        """
        if not is_valid_day(day):
            raise HoroscopeException("Invalid day. Allowed days: [today|yesterday|tomorrow]" )

        horoscopes = scrape_horoscopes_as_list(self.tree, day)
        return horoscopes

    def all_as_json(self, day):
        """gets all horoscope as json

        :returns: json of all horoscope
        """
        return json.dumps(self.all(day))
