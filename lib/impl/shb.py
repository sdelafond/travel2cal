# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

from lib.api.stay import Stay

class Shb(Stay):

  NAME = "Secure Hotel Booking"

  # This one should encompass both the stay specification, but also
  # all the specs of its nights.
  # Note that the surrounding parenthesis are important, since we both
  # split *and* search using that same regex.
  MAIN_REGEX_STR = r'''
    (Confirmation \s de \s r.servation \s - \s 
     R.f.rence \s : \s (?P<reference>.+?) \s - .+?
     R.servation: \s (?P<hotelName>.+?) \n
     -+ \s+
     Arriv.e \s : \s (?P<startDate>.+?) \n
     D.part \s : \s (?P<endDate>.+?) \n
     Dur.e \s : \s (?P<duration>.+?) \n
     Tarif \s : \s (?P<priceClass>.+?) \n
     .+?
     R.capitulatif \s+?
     -+ \s+
     (?P<roomType>.+?) \s - \s (?P<price>.+?) \n
     (?P<sub>.+?) \s+ # all the nights for that stay
     Frais.+?: \s+ (?P<fee>.+?) \s+
     Montant \s total.+?: \s+ (?P<totalPrice>.+?) \s+
     Montant \s pay..+?: \s+ (?P<prePaid>.+?) \s+
     .+?
     Adresse: \s+ (?P<address>.+?) \n\s+
     Ville: \s+ (?P<city>.+?) \n\s+
     Code \s postal: \s+ (?P<zipCode>.+?) \n\s+ 
     Pays: \s+ (?P<country>.+?)  \n\s+
     T.l.phone: \s+ (?P<phone>.+?) \n\s+
     Fax: \s+ (?P<fax>.+?) \n\s+
     Site \s internet: \s+ (?P<website>.+?) \n\s+
     Email: \s+ (?P<email>.+?) \n\s+
     .+?
     Si \s vous \s devez \s annuler)'''

  SUB_REGEX_STR = r'''
    \s*
    (?P<date>.+?): \s+
    (?P<price>[^\s]+)'''
