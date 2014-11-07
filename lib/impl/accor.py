# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.stay import Stay

class Accor(Stay):

  NAME = "Accor"

  # This one should encompass both the stay specification, but also
  # all the specs of its nights.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
     ((Num..?ro \s de \s r..?servation|Reservation \s number) \s+ : \s+ (?P<reference>[^\s]+)
     .+? (Conservez|retain|Keep) .+?
     \s\s \[\d\](?P<hotelName>(H.tel\s)? (ibis|all \s seasons|Mercure|(Suite \s )?Novotel) \s ([^\n]+)) .+?
     T..?l \s : \s (?P<phone>[^\s]+) .+? (\'\')? \s+
     (?P<address>[\d/]+[\s,].+?) ([\s\-]* \[.*?)? (?P<zipCode>\d{5}) \s+ (?P<city>[^\n]+?) ([\s\-]* \[.*?)? \s\s
     .+?
     (Du|du|from) \s (?P<startDate>[0-9/]+) \s (au|to) \s (?P<endDate>[0-9/]+) \s? , .+? (soit|i\.e\.) \s (?P<duration>\d+) \s+ (night|nuit)\(s\)
     .+?
     (?P<roomType>(Chambre|Room|Suite) \s .+?) \n\s+
     (?P<sub>.+?) # all the nights for that stay
     # (Montant \s Total|Total \s booking \s price)
     #     .+?
     (Montant \s .otal|Total \s amount|Total \s booking) \s+ .*? (?P<totalPrice>[\d\.]+ \s EUR) \n
     .+? \n \s*
     ((Le \s montant \s pr..?pay..? \s est \s de|[Aa]mount \s prepaid) \s+ (?P<prePaid>[\d\.]+) \s EUR)?
     .+?
     (Important|IMPORTANT)
     )'''

  SUB_REGEX_STR = r''' .+ '''

  TIMESTAMP_FORMAT = '%d/%m/%Y'
  TIMESTAMP_LOCALE = 'fr_FR'
