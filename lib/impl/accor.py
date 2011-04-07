# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.stay import Stay

class Accor(Stay):

  NAME = "Accor"

  # This one should encompass both the stay specification, but also
  # all the specs of its nights.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
     ((Num..?ro \s de \s r..?servation|Reservation \s number) \s+ (?P<reference>[^\s]+)
     .+? permettent\. [^\[]+
     \[\d\](?P<hotelName>[^\n]+) .+?
     T..?l \s : \s (?P<phone>.+?) \n\s*
     (?P<address>.+?) \s - \s (?P<zipCode>\d+) \s (?P<city>.+?) \s\s .*? \n\s*
     .+?
     (Du|du|from) \s (?P<startDate>[^\s]+) \s (au|to) \s (?P<endDate>[^\s]+) \s? , .+? (soit|i\.e\.) \s (?P<duration>.+?) \s (night|nuit)\(s\)
     .+?
     (?P<totalPrice>[\d\.]+ \s EUR) \n\s+
     .+?
     (?P<roomType>(Chambre|Room) \s (pour|for) \s .+?) \n\s+
     (?P<sub>.+?) # all the nights for that stay
     Important)'''

  SUB_REGEX_STR = r'''
    (?P<price>.+?)'''

  TIMESTAMP_FORMAT = '%d/%m/%Y'
  TIMESTAMP_LOCALE = 'fr_FR'
