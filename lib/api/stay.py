# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import pprint, re

class Night:
  KEYS = [ 'date', 'price' ]
  
  def __init__(self, nightDict={}):
    self.nightDict = nightDict

  def updateDict(self, d):
    self.nightDict.update(d)

  def gcal(self):
    d = {}
    d['What'] = "%(hotelName)s (%(city)s)"
    d['When'] = "from %(startDate)s to %(endDate)s"
    d['Where'] = "%(address)s %(zipCode)s %(city)s"
    d['Description'] = "phone: %(phone)s ; fax: %(fax)s ; %(email)s ; %(website)s ; %(roomType)s ; %(priceClass)s:  %(totalPrice)s including %(fee)s fee (already paid %(prePaid)s) ; reference %(reference)s"
    l = [ "%s:%s" % (k, v % self.nightDict) for k,v in d.iteritems() ]
    return ". ".join(l)

class Stay:
  KEYS = [ 'address', 'city', 'zipCode', 'phone', 'fax', 'email', 'website',
           'class', 'endDate', 'priceClass', 'startDate', 'roomType', 'price',
           'totalPrice', 'prePaid', 'reference' ]

  def __init__(self, stayDict={}, nights=[]):
    self.stayDict = stayDict
    self.nights = nights

  def addNight(self, night):
    night.updateDict(self.stayDict)
    self.nights.append(night)

  def export(self, format):
    try:
      return [ getattr(night, format.lower())() for night in self.nights ]
    except AttributeError:
      raise Exception("format '%s' does not exist." % format.lower())

  @staticmethod
  def getFactory(clsName):
    return StayFactory(clsName)

class StayFactory:
  def __init__(self, clsName):
    self.clsName = clsName
    self.stayRegex = re.compile(self.clsName.STAY_REGEX_STR,
                                re.DOTALL | re.UNICODE | re.VERBOSE)
    self.nightRegex = re.compile(self.clsName.NIGHT_REGEX_STR,
                               re.DOTALL | re.UNICODE | re.VERBOSE)

  def parse(self, str):
    stays = []
    for s in self.stayRegex.split(str):
      m = self.stayRegex.search(s)
      if m:
        stay = Stay(self.__normalizeDict(m.groupdict(), Stay.KEYS))
        for m2 in self.nightRegex.finditer(stay.stayDict['sub']):
          d = self.__normalizeDict(m2.groupdict(), Night.KEYS)
          stay.addNight(Night(d))
        stays.append(stay)
    return stays
    
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
