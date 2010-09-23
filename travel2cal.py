#!/usr/bin/env python
# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import ConfigParser, email, optparse, os, subprocess, sys

from lib.api.travel import TripFactory
from lib.api.stay import StayFactory
import lib.impl

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                                   "travel2cal.conf")

DEFAULT_FORMAT = "gcal"

DEFAULT_TYPE = "sncf"

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
parser.add_option("-t", "--type", dest="type",
                  default=DEFAULT_TYPE,
                  help="transport/stay type (available type are : 'sncf, shb'")

options, args = parser.parse_args(sys.argv[1:])

config = ConfigParser.RawConfigParser()
config.read(options.configFile)
calendar = config.get('gcal', 'name')

myType = getattr(lib.impl, options.type.capitalize())

msg = email.message_from_string(sys.stdin.read())
for part in msg.walk():
  # multipart/* are just containers
  if part.get_content_maintype() == 'multipart':
    continue
  else:
    s = None
    try:
      s = part.get_payload(decode=True).decode(msg.get_content_charset() or part.get_charset() or part.get_content_charset())
      break # stop on 1st payload successfully decoded
    except:
      continue

s = s.replace('\r\n', '\n')

# FIXME: stay factory vs. trip factory
for trip in myType.getFactory(myType).parse(s):
  for exp in trip.export(options.format):
    command = "google --cal='^%s$' calendar add '%s'" % (calendar, exp)

    if options.simulate:
      print "Would run:\n\t %s" % command
    else:
      print "Running:\n\t %s" % command
      p = subprocess.Popen(command, shell=True)
      sts = os.waitpid(p.pid, 0)[1]

    print
