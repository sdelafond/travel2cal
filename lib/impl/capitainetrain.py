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
    (Vo(?:tre)?s? \s billets? \s command.s?
    \s+ .+?
    \s+ de \s la \s commande \s est \s (?P<price>.+?)\.
    \s+ .+? R.f.rence \s : \s (?P<reservationCode>[^.]+)
    \s / \s
    (?P<reservationName>\w+)
    (?P<sub>.+?) # all the legs for that trip
    Conditions
    )'''

  SUB_REGEX_STR = r'''
    (Aller|Retour) .+?
    \s+ -+ \s+
    (?P<startDate>.+?) \s :
    .+?
    . \s (?P<startTime>[\dh]+) \s (?P<from>.+?) \n
    .+?
    . \s (?P<endTime>[\dh]+) \s (?P<to>.+?) \n
    .+?
    . \s (?P<transportType>\w+) \s (?P<transportId>\d+) \n
    .+?
    . Passager \s : .+?
    . \s Voiture \s (?P<transportSection>\d+), \s place \s (?P<seat>\d+)
    \s
    '''

  TIMESTAMP_FORMAT = '%A %d %B %Y'
  TIMESTAMP_LOCALE = 'fr_FR'
