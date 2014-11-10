# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.stay import Stay

class Bb(Stay):

  NAME = "Bb"

  # This one should encompass both the stay specification, but also
  # all the specs of its nights.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
     (Your \s booking \s no\. \s (?P<reference>[^\s]+)
     .+? Your \s stay \s : \s+
     (?P<hotelName>[^\d]+)
     # T..?l \s : \s (?P<phone>[^\s]+) .+? (\'\')? \s+
     (?P<address>[\d]+[\s,].+?) ([\s\-]* \[.*?)? (?P<zipCode>\d{5}) \s+ (?P<city>[^\n]+?) ([\s\-]* \[.*?)? \s+
     Booking \s
     (?P<duration>\d+) \s+ night.*? \s
     >From \s (?P<startDate>[0-9/]+) \s to \s (?P<endDate>[0-9/]+)
     .+?
     Price \s \d \s+
     (?P<roomType>Room \s .+?) \s\s+
     (?P<sub>.+?) # all the nights for that stay
     Total \s for \s your \s stay .*? : \s+ (?P<totalPrice>.*?) \n
     .+?
     Phone \s : \s (?P<phone>[^\*]+) \s \*
     )'''

  SUB_REGEX_STR = r''' .+ '''

  TIMESTAMP_FORMAT = '%d/%m/%Y'
  TIMESTAMP_LOCALE = 'fr_FR'
