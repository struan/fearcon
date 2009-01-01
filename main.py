#!/usr/bin/env python

import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from fearcon.db import *

class MainHandler(webapp.RequestHandler):

  def get(self):
    level = UserLevel()
    login = ''
    logout = ''
    
    if users.get_current_user():
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      if not level:
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        level.level = 3
      logout = users.create_logout_url( '/' )
      title = 'fearcon : ' + level.user.nickname()
    else:
      avgs = AverageLevel.all()
      if avgs.count() > 0:
        avg = avgs[0]
        avg_level = int( avg.total / avg.count )
      else:
        avg_level = 3
      level.level = avg_level
      login = users.create_login_url( '/' )
      title = 'fearcon : global'
        
    template_values = {
      'levels': [ 5, 4, 3, 2, 1 ],
      'current': level.level,
      'title': title,
      'login': login,
      'logout': logout
    }
    path = os.path.join(os.path.dirname(__file__), 'tmpl/index.html')
    self.response.out.write(template.render(path, template_values))



def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
