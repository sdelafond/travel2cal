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
parser.add_option("-q", "--quiet", dest="quiet",
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
parser.add_option("-n", "--name", dest="name",
                  default=None,
                  help="calendar name")

options, args = parser.parse_args(sys.argv[1:])

config = ConfigParser.RawConfigParser()
config.read(options.configFile)
calendar = options.name
if not calendar:
  calendar = config.get('gcal', 'name')
command = config.get('gcal', 'command')

msg = email.message_from_string(sys.stdin.read())
for part in msg.walk():
  # multipart/* are just containers
  if part.get_content_maintype() == 'multipart':
    continue

  s = None
  payload = part.get_payload(decode=True)
  try:
    ppCommand = config.get('preprocess', part.get_content_type())
    p1 = subprocess.Popen(["echo", "'%s'" % payload],
                          stdout=subprocess.PIPE)
    payload = subprocess.Popen(ppCommand.split(" "),
                               stdin=p1.stdout,
                               stdout=subprocess.PIPE).communicate()[0]
  except ConfigParser.NoOptionError:
    # no pre-processing for this MIME type
    if options.simulate and not options.quiet:
      print "no preprocessing"
    pass

  charset =  part.get_content_charset() or part.get_charset() or msg.get_content_charset()

  if charset:
    if options.simulate and not options.quiet:
      print "charset found: %s" % charset
    s = payload.decode(charset)
  else:
    for charset in [ 'ascii', 'iso-8859-15', 'utf-8' ]:
      try:
        if options.simulate and not options.quiet:
          print "now trying charset: %s" % charset
        s = payload.decode(charset)
      except:
        pass
  if s:
    if options.simulate and not options.quiet:
      print "decoding ok"
    break # stop on 1st payload successfully decoded

s = s.replace('\r\n', '\n')

if options.simulate and not options.quiet:
  print s

if options.type:
  types = [options.type, ]
else:
  types = TYPES

rc = -1
for myType in [ getattr(lib.impl, t.capitalize()) for t in types ]:
  if options.simulate and not options.quiet:
    print "trying type: %s" % myType
  for trip in myType.getFactory(myType).parse(s, options.simulate and not options.quiet):
    for exp in trip.export(options.format):
      if rc < 0:
        rc = 0
      cmd = "%s --cal='^%s$' quick '%s'" % (command, calendar, exp)

      if options.simulate and not options.quiet:
        print "Would run:\n\t %s" % cmd
      else:
        if not options.quiet:
          print "Running:\n\t %s" % cmd
        p = subprocess.Popen(cmd, shell=True)
        rc += os.waitpid(p.pid, 0)[1]

sys.exit(rc)
