# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import pprint, re

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
  KEYS = []

  def __init__(self, di={}):
    self.di = normalizeDict(di, self.KEYS)

  def _format(self, d):
    l = [ "%s:%s" % (k, v % self.di) for k,v in d.iteritems() ]
    return ". ".join(l)

class Main:
  KEYS = []

  SUB = Sub

  def __init__(self, di={}, subs=[]):
    self.di = normalizeDict(di, self.KEYS)
    self.subs = subs

  def addSub(self, di):
    di.update(self.di)
    self.subs.append(self.SUB(di))

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

  def parse(self, str):
    mains = []
    for s in self.mainRegex.split(str):
      m = self.mainRegex.search(s)
      if m:
        main = self.clsName(m.groupdict())
        for m2 in self.subRegex.finditer(main.di['sub']):
          main.addSub(m2.groupdict())
        mains.append(main)
    return mains
