#!/usr/bin/env python

import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from fearcon.db import *

class ChangeLevel(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      new_level = int( self.request.get('level') )
      avgs = AverageLevel.all()
      
      if avgs.count() > 0:
        avg = avgs[0]
      else:
        avg = AverageLevel()
        avg.total = 0
        avg.count = 0
      
      if not level:
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        avg.count += 1
        avg.total += new_level
      else:
        avg.total -= level.level
        avg.total += new_level
        
      level.level = new_level
      level.put()
      avg.put()
    self.response.out.write('OK')

def main():
  application = webapp.WSGIApplication([('/update', ChangeLevel)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()