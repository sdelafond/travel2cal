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
     ((Num..?ro \s de \s r..?servation|Reservation \s number) \s+ : \s+ (?P<reference>[^\s]+)
     .+? Conservez .+?
     \s\s \[\d\](?P<hotelName>[^\n]+) .+?
     T..?l \s : \s (?P<phone>[^\s]+) \s*
     (?P<address>.+?) \s - \s (?P<zipCode>\d+) \s \[.*? \n\s* (?P<city>[^\n]+)
     .+?
     (Du|du|from) \s (?P<startDate>[0-9/]+) \s (au|to) \s (?P<endDate>[0-9/]+) \s? , .+? (soit|i\.e\.) \s (?P<duration>\d+) \s+ (night|nuit)\(s\)
     .+?
     (?P<roomType>(Chambre|Room) \s (pour|for) \s .+?) \n\s+
     (?P<sub>.+?) # all the nights for that stay
     .+?
     Montant \s total
     .+?
     Montant \s Total \s TTC \s+ (?P<totalPrice>[\d\.]+ \s EUR) \n
     (?:.+?Montant \s pr..?pay..? \s+ (?P<prePaid>[\d\.]+ \s EUR) \n)?
     .+?
     Important)'''

  SUB_REGEX_STR = r''' \w '''

  TIMESTAMP_FORMAT = '%d/%m/%Y'
  TIMESTAMP_LOCALE = 'fr_FR'
