#!/usr/bin/env python

import email, os, re, subprocess, sys

class Transport:
  def __init__(self, name, regexStr):
    self.name = name
    self.regex = re.compile(regexStr, re.DOTALL | re.UNICODE | re.VERBOSE)
    self.dict = {}
    
  def extractDict(self, str):
    m = self.regex.search(str)
    if m:
      self.dict = m.groupdict()
      if not self.dict['endDate']:
        self.dict['endDate'] = ""
      for k in ('startTime', 'endTime'):
        if k in self.dict:
          self.dict[k] = self.dict[k].replace('h', ':')

  def output(self):
    s = ". ".join(["%s:%s" % (k, v % self.dict) for k,v in self.format().iteritems()])
    return s.replace("'", " ").replace('\n', '')

class Sncf(Transport):
  REGEX_STR = r'''
    -+\s+
    TRAIN .+? \s+\|\s+
    (?P<from>.+?) \s => \s (?P<to>.+?) \s+\|\s+.+?\s\|\s
    (?P<price>.+?) \s+ -+ \s+
    D.part \s+ : \s+ (?P<stationFrom>.+?) \s-\s
    (?P<startTime>[\dh]+) \s-\s
    (?P<startDate>[\d/]+) \s
    Arriv.e \s+ : \s+ (?P<stationTo>.+?) \s-\s
    (?P<endTime>[\dh]+) \s(-\s
    (?P<endDate>[\d/]+) \s)?
    (?P<trainType>\w+) \s-\s
    (?P<trainNumber>\d+) \s-\s
    (?P<class>.+?) \n\s-+\s
    .+?
    (?P<priceClass>.+?) \n\n
    Voiture \s (?P<car>\d+) \s-\s
    Place \s (?P<seat>\d+) \n
    (?P<seatType>.+?) \n .+?
    dossier \s+ : \s+ (?P<reservationCode>.{6}) \s .+?
    associ. \s+ : \s+ (?P<reservationName>.+?) \s'''

  def __init__(self):
    Transport.__init__(self, "SNCF", self.REGEX_STR)

  def format(self):
    d = {}
    d['What'] = "%(trainType)s %(from)s - %(to)s"
    d['When'] = "on %(startDate)s %(startTime)s - %(endTime)s"
    d['Where'] = "%(stationFrom)s -> %(stationTo)s"
    d['Description'] = "%(reservationCode)s %(reservationName)s ; %(trainType)s %(trainNumber)s ;Voiture %(car)s Place %(seat)s (%(seatType)s) ; %(class)s - %(priceClass)s ; %(price)s"
    return d
  
msg = email.message_from_string(sys.stdin.read())
s = msg.get_payload(decode=True).decode(msg.get_content_charset())

sncf = Sncf()
sncf.extractDict(s)

command = "google --cal='^Seb$' calendar add '%s'" % sncf.output()
print command

p = subprocess.Popen(command, shell=True)
sts = os.waitpid(p.pid, 0)[1]
