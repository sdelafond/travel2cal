# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.stay import Stay

class Citea(Stay):

  NAME = "Citea"

  # This one should encompass both the stay specification, but also
  # all the specs of its nights.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
    (Confirmation: \s (?P<reference>.+?) \s+
     .+?
     cancel \s your \s reservation \s+
     (?P<hotelName>[^\n]+) \n\s*
     (?P<address>.+?) \n\s*
     (?P<city>.+?), \s+
     (?P<zipCode>.+?) \n\s*
     (?P<country>.+?) \n\s*
     T.l: \s+ (?P<phone>.+?) \n\s*
     Fax: \s+ (?P<fax>.+?) \n\s*
     e-mail: \s+ (?P<email>.+?) \n
     .+?
     Total \s Price: \s+ (?P<totalPrice>.+?) \n\s+
     .+?
     Room \s Type: \s+ (?P<roomType>.+?) \s+
     Type \s of \s bed: \s+ (?P<bedType>.+?) \n
     .+?
     Arrival \s Date: \s+ (?P<startDate>.+?) \n
     Departure \s Date: \s+ (?P<endDate>.+?) \n
     Stay: \s+ (?P<duration>.+?) \s+
     Pricing
     (?P<sub>.+?) # all the nights for that stay
     nice \s stay)'''

  SUB_REGEX_STR = r'''
    \s*
    (?P<date>.+?): \s+
    (?P<price>[^\s]+)'''
