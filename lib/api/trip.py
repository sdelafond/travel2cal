# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import re
from generic import Main, Sub

class Leg(Sub):
  KEYS = [ 'class', 'endDate', 'endTime', 'from', 'priceClass',
           'seat', 'seatType', 'startDate',
           'startTime', 'to', 'transportId', 'transportSection',
           'transportType' ]

  def updateDict(self, d):
    self.legDict.update(d)

  def gcal(self):
    d = {}
    d['What'] = "%(transportType)s %(from)s - %(to)s | c%(transportSection)ss%(seat)s"
    d['When'] = "on %(startDate)s %(startTime)s - %(endTime)s"
    d['Where'] = "%(from)s -> %(to)s"
    d['Description'] = "Car %(transportSection)s Seat %(seat)s (%(seatType)s) ; %(reservationCode)s %(reservationName)s ; %(transportType)s %(transportId)s ; %(class)s - %(priceClass)s ; %(price)s (%(cityFrom)s -> %(cityTo)s %(roundTrip)s)"
    return self._format(d)

class Trip(Main):
  KEYS = [ 'cityFrom', 'cityTo', 'price',
           'reservationCode', 'reservationName', 'roundTrip' ]

  SUB = Leg
