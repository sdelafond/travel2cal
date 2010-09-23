# coding=utf-8

# Sébastien Delafond <sdelafond@gmail.com>

import re
from generic import Main, Sub

class Night(Sub):
  KEYS = [ 'date', 'price' ]
  
  def gcal(self):
    d = {}
    d['What'] = "%(hotelName)s (%(city)s)"
    d['When'] = "from %(startDate)s to %(endDate)s"
    d['Where'] = "%(address)s %(zipCode)s %(city)s"
    d['Description'] = "phone: %(phone)s ; fax: %(fax)s ; %(email)s ; %(website)s ; %(roomType)s ; %(priceClass)s:  %(totalPrice)s including %(fee)s fee (already paid %(prePaid)s) ; reference %(reference)s"
    return self._format(d)
    
class Stay(Main):
  KEYS = [ 'address', 'city', 'zipCode', 'phone', 'fax', 'email', 'website',
           'class', 'endDate', 'priceClass', 'startDate', 'roomType', 'price',
           'totalPrice', 'prePaid', 'reference', 'fee', 'bedType' ]

  SUB = Night
