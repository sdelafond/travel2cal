#!/usr/bin/env python

import email, optparse, os, re, subprocess, sys

class Transport:

  KEYS = [ 'transportSection', 'cityFrom', 'cityTo', 'class', 'endDate', 'endTime',
           'from', 'price', 'priceClass', 'reservationCode',
           'reservationName', 'seat', 'seatType', 'startDate',
           'startTime', 'to', 'transportId', 'transportType' ]
  
  def __init__(self, name, regexStr):
    self.name = name
    self.regex = re.compile(regexStr, re.DOTALL | re.UNICODE | re.VERBOSE)
    self.dict = {}
    
  def extractDict(self, str):
    m = self.regex.search(str)
    if m:
      self.dict = m.groupdict()
    self.normalizeDict()
    
  def normalizeDict(self):
    if not self.dict['endDate']:
      self.dict['endDate'] = ""

    for k in ('startTime', 'endTime'):
      if k in self.dict:
        self.dict[k] = self.dict[k].replace('h', ':')

    for k in self.dict:
      self.dict[k] = self.dict[k].replace("'", " ").replace('\n', '')
      
  def getGcalQuickAdd(self):
    d = {}
    d['What'] = "%(transportType)s %(cityFrom)s - %(cityTo)s"
    d['When'] = "on %(startDate)s %(startTime)s - %(endTime)s"
    d['Where'] = "%(from)s -> %(to)s"
    d['Description'] = "%(reservationCode)s %(reservationName)s ; %(transportType)s %(transportId)s ; Wagon %(transportSection)s Seat %(seat)s (%(seatType)s) ; %(class)s - %(priceClass)s ; %(price)s"
    l = [ "%s:%s" % (k, v % self.dict)
          for k,v in d.iteritems() ]
    return ". ".join(l)

class Sncf(Transport):

  REGEX_STR = r'''
    TRAIN .+? \s+\|\s+
    (?P<cityFrom>.+?) \s => \s (?P<cityTo>.+?) \s+\|\s+.+?\s\|\s
    (?P<price>.+?) \s+ -+ \s+
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
    (?P<seatType>.+?) \n .+?
    dossier \s+ : \s+ (?P<reservationCode>.{6}) \s .+?
    associ. \s+ : \s+ (?P<reservationName>.+?) \s'''

  def __init__(self):
    Transport.__init__(self, "SNCF", self.REGEX_STR)


# main
parser = optparse.OptionParser()
parser.add_option("-s", "--simulate", dest="simulate",
                  action="store_true", default=False,
                  help="Simulation mode")

options, args = parser.parse_args(sys.argv[1:])

msg = email.message_from_string(sys.stdin.read())
s = msg.get_payload(decode=True).decode(msg.get_content_charset())

sncf = Sncf()
sncf.extractDict(s)

print sncf.getGcalQuickAdd()

if not options.simulate:
  command = "google --cal='^Seb$' calendar add '%s'" % sncf.getGcalQuickAdd()
  print "Running %s" % command
  p = subprocess.Popen(command, shell=True)
  sts = os.waitpid(p.pid, 0)[1]
