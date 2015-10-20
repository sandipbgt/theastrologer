# -*- coding: utf-8 -*-
"""
    theastrologer
    ~~~~~~~~~~~~~

    theastrologer module
"""

from datetime import date, timedelta
from requests import get
from requests.exceptions import RequestException, Timeout
from lxml import etree
from six import u

__version__ = '0.1.0'

def is_valid_sunsign(sunsign):
    sunsigns = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    if sunsign not in sunsigns:
        return False
    return True

def is_valid_day(day):
    days = ['today', 'yesterday', 'tomorrow']
    if day not in days:
        return False
    return True

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

    def __init__(self, sunsign=None):
        """
        Create a Horoscope
        """

        if not is_valid_sunsign(sunsign):
            raise HoroscopeException("Invalid horoscope sunsign")

        self.sunsign = sunsign.lower()
        self.url = "http://new.theastrologer.com/" + self.sunsign
        self.parser = etree.HTMLParser()
        self.date_today = date.today()
        try:
            self.html_resp = get(self.url)
        except Timeout as e:
            raise HoroscopeException(e)
        except RequestException as e:
            raise HoroscopeException(e)
        self.tree = etree.fromstring(self.html_resp.text, self.parser)

    def _get_horoscope(self, day='today'):
        """gets a horoscope from site html

        :param day: day for which to get horoscope. Default is 'today'

        :returns: dictionary of horoscope details
        """
        if not is_valid_day(day):
            raise HoroscopeException("Invalid day. Allowed days: [today|yesterday|tomorrow]" )

        horoscope = str(self.tree.xpath('//*[@id="%s"]/p/text()' % day)[0])

        if day is 'yesterday':
            date = self.date_today - timedelta(days=1)
        elif day is 'today':
            date = self.date_today
        elif day is 'tomorrow':
            date = self.date_today + timedelta(days=1)

        return {
            'date': date.strftime("%Y-%m-%d"),
            'sunsign': self.sunsign.capitalize(),
            'horoscope': horoscope,
            'meta': self._get_horoscope_meta(day),
        }

    def _get_horoscope_meta(self, day='today'):
        """gets a horoscope meta from site html

        :param day: day for which to get horoscope meta. Default is 'today'

        :returns: dictionary of horoscope mood details
        """
        if not is_valid_day(day):
            raise HoroscopeException("Invalid day. Allowed days: [today|yesterday|tomorrow]" )

        return {
            'intensity': str(self.tree.xpath('//*[@id="%s"]/div[3]/div[1]/p[1]/text()' % day)[0]).replace(": ", ""),
            'mood': str(self.tree.xpath('//*[@id="%s"]/div[3]/div[1]/p[2]/text()' % day)[0]).replace(": ", ""),
            'keywords': str(self.tree.xpath('//*[@id="%s"]/div[3]/div[2]/p[1]/text()' % day)[0]).replace(": ", ""),
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
