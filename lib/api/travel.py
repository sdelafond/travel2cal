# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import re

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
      raise Exception("format '%s' does not exist." % format.lower())

  @staticmethod
  def getFactory(clsName):
    return TripFactory(clsName)

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
        for m2 in self.legRegex.finditer(trip.tripDict['sub']):
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
      if not k == 'sub':
        d[k] = re.sub(r"['\n]", ' ', d[k])
        d[k] = re.sub(r'(<.+?>|&\w+?;)', '', d[k]) # crude unhtml

    return d
