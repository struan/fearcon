#!/usr/bin/env python

import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from fearcon.db import *

class ChangeUserLevel(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      new_level = int( self.request.get('level') )
      
      if not level:
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        level.nick = level.user.nickname(
        
      level.level = new_level
      level.put()
    self.response.out.write('OK')
    
class ChangeTotalLevel(webapp.RequestHandler):
  def post(self):
      old_level = int( self.request.get('old_level') )
      new_level = int( self.request.get('new_level') )
      avgs = db.Query(AverageLevel)

      if avgs:
        avg = avgs.get()
      else:
        avg = AverageLevel()
        avg.total = 0
        avg.count = 0
        
      if old_level == 0:
        avg.count += 1
        avg.total += new_level
      else:
        total = avg.total
        total -= old_level
        total += new_level
        avg.total = total

      avg.put()
    self.response.out.write('OK')

def main():
  application = webapp.WSGIApplication([('/update_user', ChangeUserLevel),
                                        ('/update_total', ChangeTotalLevel)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()