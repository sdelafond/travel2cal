# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.trip import Trip

class Capitainetrain(Trip):

  NAME = "Capitainetrain"

  # This one should encompass both the trip specification, but also
  # all the specs of its legs.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
    (Vos \s billets \s command.s
    \s+ .+?
    \s+ de \s la \s commande \s est \s (?P<price>.+?)\.
    \s+ .+? votre \s e-billet \s est \s (?P<reservationCode>.{6})
    \s / \s
    (?P<reservationName>.+?)\.
    (?P<sub>.+?) # all the legs for that trip
    Conditions
    )'''

  SUB_REGEX_STR = r'''
    \d+\. \s (?P<from>.+?) \s .+?> \s (?P<to>.+?)
    \s+ -+ \s+
    D.part \s (?P<startDate>.+?),
    .+?
    \* \s (?P<startTime>[\d:]+) \s : \s
    .+?
    \* \s (?P<endTime>[\d:]+) \s : \s
    .+?
    \* \s (?P<transportType>.+?) \s SNCF \s n. \s (?P<transportId>\d+)
    \s+
    \* \s Voiture \s (?P<transportSection>\d+), \s place \s (?P<seat>\d+)
    \s
    '''

  TIMESTAMP_FORMAT = '%A %d %B %Y'
  TIMESTAMP_LOCALE = 'fr_FR'
