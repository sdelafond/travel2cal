#!/usr/bin/env python
# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import ConfigParser, email, optparse, os, re, subprocess, sys

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                                   "travel2cal.conf")

DEFAULT_FORMAT = "gcal"

class Leg:
  KEYS = [ 'class', 'endDate', 'endTime', 'from', 'priceClass',
           'seat', 'seatType', 'startDate',
           'startTime', 'to', 'transportId', 'transportSection',
           'transportType' ]

  def __init__(self, legDict={}):
    self.legDict = legDict

  def updateDict(self, d):
    self.legDict.update(d)

  def gcal(self):
    d = {}
    d['What'] = "%(transportType)s %(from)s - %(to)s"
    d['When'] = "on %(startDate)s %(startTime)s - %(endTime)s"
    d['Where'] = "%(from)s -> %(to)s"
    d['Description'] = "%(reservationCode)s %(reservationName)s ; %(transportType)s %(transportId)s ; Wagon %(transportSection)s Seat %(seat)s (%(seatType)s) ; %(class)s - %(priceClass)s ; %(price)s (%(cityFrom)s -> %(cityTo)s %(roundTrip)s)"
    l = [ "%s:%s" % (k, v % self.legDict) for k,v in d.iteritems() ]
    return ". ".join(l)

class Trip:
  KEYS = [ 'cityFrom', 'cityTo', 'price',
           'reservationCode', 'reservationName', 'roundTrip' ]
  
  def __init__(self, tripDict={}, legs=[]):
    self.tripDict = tripDict
    self.legs = legs

  def addLeg(self, leg):
    leg.updateDict(self.tripDict)
    self.legs.append(leg)

  def export(self, format):
    try:
      return [ getattr(leg, format.lower())() for leg in self.legs ]
    except AttributeError:
      print "format '%s' does not exist." % format.lower()
      sys.exit(1)

class TripFactory:
  def __init__(self, clsName):
    self.clsName = clsName
    self.tripRegex = re.compile(self.clsName.TRIP_REGEX_STR,
                                re.DOTALL | re.UNICODE | re.VERBOSE)
    self.legRegex = re.compile(self.clsName.LEG_REGEX_STR,
                               re.DOTALL | re.UNICODE | re.VERBOSE)

  def parse(self, str):
    trips = []
    for s in self.tripRegex.split(str):
      m = self.tripRegex.search(s)
      if m:
        trip = Trip(self.__normalizeDict(m.groupdict(), Trip.KEYS))
        for m2 in self.legRegex.finditer(s):
          d = self.__normalizeDict(m2.groupdict(), Leg.KEYS)
          trip.addLeg(Leg(d))
        trips.append(trip)
    return trips
    
  def __normalizeDict(self, d, keys):
    for k in keys:
      if not k in d or not d[k]: # create missing keys
        d[k] = ""
    for k in ('startTime', 'endTime'):
      if k in d:
        d[k] = d[k].replace('h', ':') # needed by gcal
    for k in d:
      d[k] = re.sub(r"['\n]", ' ', d[k])
      d[k] = re.sub(r'(<.+?>|&\w+?;)', '', d[k]) # crude unhtml

    return d

class Sncf(Trip):

  NAME = "SNCF"

  # This one should encompass both the trip specification, but also
  # all the specs of its legs.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  TRIP_REGEX_STR = r'''
    (TRAIN (?P<roundTrip>.+?)
    \s+\|\s+
    (?P<cityFrom>.+?) \s <?=> \s (?P<cityTo>.+?)
    \s+\|\s+.+?\s\|\s
    (?P<price>.+?)
    \s+ -+ \s+ 
    .+? # all the legs for that trip
    dossier \s+ : \s+ (?P<reservationCode>.{6}) \s .+?
    associ. \s+ : \s+ (?P<reservationName>.+?) \s)'''

  LEG_REGEX_STR = r'''
    D.part \s+ : \s+ (?P<from>.+?) \s-\s
    (?P<startTime>[\dh]+) \s-\s
    (?P<startDate>[\d/]+) \s
    Arriv.e \s+ : \s+ (?P<to>.+?) \s-\s
    (?P<endTime>[\dh]+) \s(-\s
    (?P<endDate>[\d/]+) \s)?
    (?P<transportType>\w+) \s-\s
    (?P<transportId>\d+) \s-\s
    (?P<class>.+?) \n\s-+\s
    .+?
    (?P<priceClass>.+?) \n\n
    Voiture \s (?P<transportSection>\d+) \s-\s
    Place \s (?P<seat>\d+) \n
    (?P<seatType>.+?) \n .+?'''


# main
parser = optparse.OptionParser()
parser.add_option("-s", "--simulate", dest="simulate",
                  action="store_true", default=False,
                  help="simulation mode")
parser.add_option("-c", "--config-file", dest="configFile",
                  default=DEFAULT_CONFIG_FILE,
                  help="config-file location")
parser.add_option("-f", "--format", dest="format",
                  default=DEFAULT_FORMAT,
                  help="output format style (available styles are : 'gcal'")

options, args = parser.parse_args(sys.argv[1:])

config = ConfigParser.RawConfigParser()
config.read(options.configFile)
calendar = config.get('gcal', 'name')

msg = email.message_from_string(sys.stdin.read())
s = msg.get_payload(decode=True).decode(msg.get_content_charset())

for trip in TripFactory(Sncf).parse(s):
  for exp in trip.export(options.format):
    command = "google --cal='^%s$' calendar add '%s'" % (calendar, exp)

    if options.simulate:
      print "Would run:\n\t %s" % command
    else:
      print "Running:\n\t %s" % command
      p = subprocess.Popen(command, shell=True)
      sts = os.waitpid(p.pid, 0)[1]

    print
