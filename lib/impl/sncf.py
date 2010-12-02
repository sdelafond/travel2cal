# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.trip import Trip

class Sncf(Trip):

  NAME = "SNCF"

  # This one should encompass both the trip specification, but also
  # all the specs of its legs.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
    (TRAIN (?P<roundTrip>.+?)
    \s+\|\s+
    (?P<cityFrom>.+?) \s <?=> \s (?P<cityTo>.+?)
    \s+\|\s+.+?\s\|\s
    (?P<price>.+?)
    \s+ -+ \s+ 
    (?P<sub>.+?) # all the legs for that trip
    dossier \s+ : \s+ (?P<reservationCode>.{6}) \s .+?
    associ. \s+ : \s+ (?P<reservationName>.+?) \s)'''

  SUB_REGEX_STR = r'''
    D.part \s+ : \s+ (?P<from>.+?) \s-\s
    (?P<startTime>[\dh]+) \s-\s
    (?P<startDate>[\d/]+) \s
    Arriv.e \s+ : \s+ (?P<to>.+?) \s-\s
    (?P<endTime>[\dh]+) \s(-\s
    (?P<endDate>[\d/]+) \s)?
    (?P<transportType>[^-]+) \s-\s
    (?P<transportId>\d+) \s-\s
    (?P<class>.+?) \n\s-+\s
    .+?
    (?P<priceClass>.+?) \n\n
    Voiture \s (?P<transportSection>\d+) \s-\s
    Place \s (?P<seat>\d+) \n
    (?P<seatType>.+?)'''

  TIMESTAMP_FORMAT = '%d/%m/%Y'
  TIMESTAMP_LOCALE = 'fr_FR'
