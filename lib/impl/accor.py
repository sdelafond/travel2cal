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
    (Num.ro \s de \s r.servation \s+ (?P<reference>[^\s]+)
    .+?
     \[\d\](?P<hotelName>[^\n]+) \n\s*
     T.l \s : \s (?P<phone>.+?) \n\s*
     (?P<address>.+?) \s - \s (?P<zipCode>\d+) \s (?P<city>.+?) \s\s .*? \n\s*
     .+?
     Du \s (?P<startDate>[^\s]+) \s au \s (?P<endDate>[^\s]+), .+? soit \s (?P<duration>.+?) \s nuit\(s\)
     .+?
     (?P<totalPrice>[\d\.]+ \s EUR) \n\s+
     .+?
     (?P<roomType>Chambre \s pour \s .+?) \n\s+
     (?P<sub>.+?) # all the nights for that stay
     A-Club)'''

  SUB_REGEX_STR = r'''
    (?P<price>.+?)'''
