# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import locale, re, subprocess
from datetime import datetime
from subprocess import Popen, PIPE

output = Popen(("locale", "-a"), stdout=PIPE).communicate()[0]
LOCALES = output.split('\n')

def normalizeDict(d, keys):
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

class Sub:
  # overloaded in lib/api/*
  KEYS = []

  def __init__(self, cls, di={}):
    self.cls = cls
    self.di = self._normalizeDict(di)

  def _normalizeDict(self, di):
    if self.cls.TIMESTAMP_FORMAT:
      oldLocale = locale.getlocale()

      loc = None
      for l in LOCALES:
        if l.startswith(self.cls.TIMESTAMP_LOCALE):
          loc = l

      if not loc:
        raise Exception("No supported locale found to match '%s'" % self.cls.TIMESTAMP_LOCALE)

      for key in ('startDate', 'endDate'):
        if not di.get(key):
          continue
        locale.setlocale(locale.LC_ALL, loc)
        ts = datetime.strptime(di[key].encode('utf-8'), self.cls.TIMESTAMP_FORMAT)
        locale.setlocale(locale.LC_ALL, oldLocale)
        di[key] = datetime.strftime(ts, '%d %b %Y')

    return normalizeDict(di, self.KEYS)

  def _format(self, d):
    l = [ "%s:%s" % (k, v % self.di) for k,v in d.iteritems() ]
    return ". ".join(l)

  def __cmp__(self, o):
    return (isinstance(o, self.__class__) and cmp(self.di, o.di))

class Main:
  # overloaded in lib/api/*
  SUB = Sub
  KEYS = []

  # overloaded in lib/impl/*
  MAIN_REGEX_STR = ""
  SUB_REGEX_STR = ""
  TIMESTAMP_FORMAT = ""
  TIMESTAMP_LOCALE = ""

  def __init__(self, di={}, subs=[]):
    self.di = self._normalizeDict(di)
    self.subs = subs

  def _normalizeDict(self, di):
    return normalizeDict(di, self.KEYS)

  def addSub(self, di):
    di.update(self.di)
    sub = self.SUB(self.__class__, di)
    if not sub in self.subs:
      self.subs.append(sub)
      
  def export(self, format):
    try:
      return [ getattr(sub, format.lower())() for sub in self.subs ]
    except AttributeError:
      raise
      raise Exception("format '%s' does not exist." % format.lower())

  @staticmethod
  def getFactory(clsName):
    return MainFactory(clsName)

class MainFactory:
  def __init__(self, clsName):
    self.clsName = clsName
    self.mainRegex = re.compile(self.clsName.MAIN_REGEX_STR,
                                re.DOTALL | re.UNICODE | re.VERBOSE)
    self.subRegex = re.compile(self.clsName.SUB_REGEX_STR,
                               re.DOTALL | re.UNICODE | re.VERBOSE)

  def parse(self, str, simulate):
    mains = []
    for s in self.mainRegex.split(str):
      if not s:
        s = ""
      m = self.mainRegex.search(s)
      if m:
        main = self.clsName(m.groupdict())
        if simulate:
          print "match for main regex"
          print main.di
        for m2 in self.subRegex.finditer(main.di['sub']):
          main.addSub(m2.groupdict())
          if simulate:
            print "match for subregex"
            print m2.groupdict()
        mains.append(main)
    return mains
