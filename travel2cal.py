#!/usr/bin/env python
# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import ConfigParser, email, optparse, os, subprocess, sys

from lib.api.travel import TripFactory
from lib.impl import *

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                                   "travel2cal.conf")

DEFAULT_FORMAT = "gcal"

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

for trip in TripFactory(sncf.Sncf).parse(s):
  for exp in trip.export(options.format):
    command = "google --cal='^%s$' calendar add '%s'" % (calendar, exp)

    if options.simulate:
      print "Would run:\n\t %s" % command
    else:
      print "Running:\n\t %s" % command
      p = subprocess.Popen(command, shell=True)
      sts = os.waitpid(p.pid, 0)[1]

    print
