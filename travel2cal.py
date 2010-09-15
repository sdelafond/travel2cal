#!/usr/bin/env python
# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import ConfigParser, email, optparse, os, re, subprocess, sys

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                                   "travel2cal.conf")

class Transport:

  KEYS = [ 'cityFrom', 'cityTo', 'class', 'endDate', 'endTime',
           'from', 'price', 'priceClass', 'reservationCode',
           'reservationName', 'seat', 'seatType', 'startDate',
           'startTime', 'to', 'transportId', 'transportSection',
           'transportType' ]
  
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
    for k in self.KEYS:
      if not k in self.dict or not self.dict[k]:
        self.dict[k] = ""

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
parser.add_option("-c", "--config-file", dest="configFile",
                  default=DEFAULT_CONFIG_FILE,
                  help="Config-file location")

options, args = parser.parse_args(sys.argv[1:])

msg = email.message_from_string(sys.stdin.read())
s = msg.get_payload(decode=True).decode(msg.get_content_charset())

sncf = Sncf()
sncf.extractDict(s)

print sncf.getGcalQuickAdd()

config = ConfigParser.RawConfigParser()
config.read(options.configFile)

calendar = config.get('gcal', 'name')
      
command = "google --cal='^%s$' calendar add '%s'" % (calendar,
                                                     sncf.getGcalQuickAdd())

if options.simulate:
  print "Would run:\n\t %s" % command
else:
  print "Running:\n\t %s" % command
  p = subprocess.Popen(command, shell=True)
  sts = os.waitpid(p.pid, 0)[1]
