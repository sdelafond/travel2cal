#!/usr/bin/env python
# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import ConfigParser, email, optparse, os, re, subprocess, sys

import lib.impl

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                                   "travel2cal.conf")

DEFAULT_FORMAT = "gcal"

TYPES = [ t.lower() for t in lib.impl.__all__ ]

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
                  default=None,
                  help="trip/stay type (available type are : %s" % (TYPES,))

options, args = parser.parse_args(sys.argv[1:])

config = ConfigParser.RawConfigParser()
config.read(options.configFile)
calendar = config.get('gcal', 'name')
ppCommand = config.get('preprocess', 'command')

msg = email.message_from_string(sys.stdin.read())
for part in msg.walk():
  # multipart/* are just containers
  if part.get_content_maintype() == 'multipart':
    continue
  else:
    s = None
    payload = part.get_payload(decode=True)
    charset = msg.get_content_charset() or part.get_charset() or part.get_content_charset()
    if charset:
      s = payload.decode(charset)
    else:
      for charset in [ 'ascii', 'iso-8859-15', 'utf-8' ]:
        try:
          s = payload.decode(charset)
        except:
          pass
    if s:
      break # stop on 1st payload successfully decoded

s = s.replace('\r\n', '\n')
p1 = subprocess.Popen(["echo", "'%s'" % s], stdout=subprocess.PIPE)
s = subprocess.Popen(ppCommand.split(" "), stdin=p1.stdout, stdout=subprocess.PIPE).communicate()[0]
s = s.decode(charset)
#print s

if options.type:
  types = [options.type, ]
else:
  types = TYPES

for myType in [ getattr(lib.impl, t.capitalize()) for t in types ]:
  for trip in myType.getFactory(myType).parse(s):
    for exp in trip.export(options.format):
      command = "google --cal='^%s$' calendar add '%s'" % (calendar, exp)

      if options.simulate:
        print "Would run:\n\t %s" % command
      else:
        print "Running:\n\t %s" % command
        p = subprocess.Popen(command, shell=True)
        sts = os.waitpid(p.pid, 0)[1]
